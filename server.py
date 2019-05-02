#!/usr/bin/env python3
"""
Usage:
    server.py [--nodb | --db TYPE]

Options:
    --nodb      Don't use a database (Use a mock.Mock). Caution: Will break things.
    --db TYPE   Use TYPE database driver [default: QMYSQL]
"""

import asyncio
import logging
import signal
import socket

import server
import server.config as config
from server.config import (DB_LOGIN, DB_NAME, DB_PASSWORD, DB_PORT, DB_SERVER,
                           TWILIO_ACCOUNT_SID)
from server.ice_servers.nts import TwilioNTS
from server.matchmaker import MatchmakerQueue

if __name__ == '__main__':
    logger = logging.getLogger()
    stderr_handler = logging.StreamHandler()
    stderr_handler.setFormatter(logging.Formatter('%(levelname)-8s %(name)-30s %(message)s'))
    logger.addHandler(stderr_handler)
    logger.setLevel(config.LOG_LEVEL)

    try:
        def signal_handler(signal, frame):
            logger.info("Received signal, shutting down")
            if not done.done():
                done.set_result(0)

        loop = asyncio.get_event_loop()
        done = asyncio.Future()

        from docopt import docopt

        args = docopt(__doc__, version='FAF Server')

        if config.ENABLE_STATSD:
            logger.info("Using StatsD server: ".format(config.STATSD_SERVER))

        # Make sure we can shutdown gracefully
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        engine_fut = asyncio.ensure_future(
            server.db.connect_engine(
                host=DB_SERVER,
                port=int(DB_PORT),
                user=DB_LOGIN,
                password=DB_PASSWORD,
                maxsize=10,
                db=DB_NAME,
                loop=loop
            )
        )
        engine = loop.run_until_complete(engine_fut)

        twilio_nts = None
        if TWILIO_ACCOUNT_SID:
            twilio_nts = TwilioNTS()
        else:
            logger.warning(
                "Twilio is not set up. You must set TWILIO_ACCOUNT_SID and TWILIO_TOKEN to use the Twilio ICE servers.")

        players_online = server.app._get_service("player_service")
        game_service = server.app._get_service("game_service")

        ctrl_server = loop.run_until_complete(server.run_control_server(loop, players_online, game_service))

        lobby_server = server.run_lobby_server(
            address=('', 8001),
            nts_client=twilio_nts,
            matchmaker_queue=MatchmakerQueue('ladder1v1', game_service=game_service),
            loop=loop
        )

        for sock in lobby_server.sockets:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        loop.run_until_complete(done)
        players_online.broadcast_shutdown()

        # Close DB connections
        engine.close()
        loop.run_until_complete(engine.wait_closed())

        loop.close()

    except Exception as ex:
        logger.exception("Failure booting server {}".format(ex))
