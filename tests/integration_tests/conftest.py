import asyncio
import hashlib
import logging
from unittest import mock

import pytest
from server import run_lobby_server
from server.protocol import QDataStreamProtocol
from server.matchmaker import MatchmakerQueue


@pytest.fixture
def lobby_server(request, loop, game_service, mocker):
    mocker.patch("server.player_service.PlayerService.is_uniqueid_exempt", side_effect=lambda id: True)

    ctx = run_lobby_server(
        address=('127.0.0.1', None),
        matchmaker_queue=MatchmakerQueue('ladder1v1', game_service),
        nts_client=None,
        loop=loop
    )

    def fin():
        ctx.close()
        loop.run_until_complete(ctx.wait_closed())

    request.addfinalizer(fin)

    return ctx


async def connect_client(server):
    return QDataStreamProtocol(
        *(await asyncio.open_connection(*server.sockets[0].getsockname()))
    )


async def perform_login(proto, credentials):
    login, pw = credentials
    pw_hash = hashlib.sha256(pw.encode('utf-8'))
    proto.send_message({
        'command': 'hello',
        'version': '1.0.0-dev',
        'user_agent': 'faf-client',
        'login': login,
        'password': pw_hash.hexdigest(),
        'unique_id': 'some_id'
    })
    await proto.drain()


async def read_until(proto, pred):
    while True:
        msg = await proto.read_message()
        try:
            if pred(msg):
                return msg
        except (KeyError, ValueError):
            logging.getLogger().info("read_until predicate raised during message: {}".format(msg))
            pass


async def get_session(proto):
    proto.send_message({'command': 'ask_session', 'user_agent': 'faf-client', 'version': '0.11.16'})
    await proto.drain()
    msg = await proto.read_message()

    return msg['session']


async def connect_and_sign_in(credentials, lobby_server):
    proto = await connect_client(lobby_server)
    session = await get_session(proto)
    await perform_login(proto, credentials)
    hello = await read_until(proto, lambda msg: msg['command'] == 'welcome')
    player_id = hello['id']
    return player_id, session, proto
