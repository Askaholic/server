"""
Forged Alliance Forever server project

Copyright (c) 2012-2014 Gael Honorez
Copyright (c) 2015-2016 Michael Søndergaard <sheeo@faforever.com>

Distributed under GPLv3, see license.txt
"""

import json
import logging
from typing import Any, Dict, Optional

import aiomeasures
from . import config as config
from .games.game import GameState, VisibilityState
from .stats.game_stats_service import GameStatsService
from .gameconnection import GameConnection
from .ice_servers.nts import TwilioNTS
from .lobbyconnection import LobbyConnection
from .protocol import QDataStreamProtocol
from .servercontext import ServerContext
from .geoip_service import GeoIpService
from .player_service import PlayerService
from .game_service import GameService
from .ladder_service import LadderService
from .control import init as run_control_server
from .main import app
from .matchmaker import MatchmakerQueue

__version__ = '0.9.17'
__author__ = 'Chris Kitching, Dragonfire, Gael Honorez, Jeroen De Dauw, Crotalus, Michael Søndergaard, Michel Jung'
__contact__ = 'admin@faforever.com'
__license__ = 'GPLv3'
__copyright__ = 'Copyright (c) 2011-2015 ' + __author__


__all__ = [
    'GameConnection',
    'GameService',
    'GameStatsService',
    'LadderService',
    'run_lobby_server',
    'run_control_server',
    'games',
    'control',
    'abc',
    'protocol'
]

DIRTY_REPORT_INTERVAL = 1  # Seconds
stats = None

if not config.ENABLE_STATSD:
    from . import fake_statsd
    stats = fake_statsd.DummyConnection()
else:
    stats = aiomeasures.StatsD(config.STATSD_SERVER)


def encode_message(message: str):
    # Crazy evil encoding scheme
    return QDataStreamProtocol.pack_message(message)


def encode_dict(d: Dict[Any, Any]):
    return encode_message(json.dumps(d))


def encode_players(players):
    return encode_dict({
        'command': 'player_info',
        'players': [player.to_dict() for player in players]
    })


def encode_queues(queues):
    return encode_dict({
        'command': 'matchmaker_info',
        'queues': [queue.to_dict() for queue in queues]
    })


@app.inject
def run_lobby_server(
    game_service: GameService,
    geoip_service: GeoIpService,
    player_service: PlayerService,
    address: (str, int),
    loop,
    nts_client: Optional[TwilioNTS],
    matchmaker_queue: MatchmakerQueue
) -> ServerContext:
    """
    Run the lobby server
    """

    def report_dirties():
        try:
            dirty_games = game_service.dirty_games
            dirty_queues = game_service.dirty_queues
            dirty_players = player_service.dirty_players
            game_service.clear_dirty()
            player_service.clear_dirty()

            if len(dirty_queues) > 0:
                ctx.broadcast_raw(encode_queues(dirty_queues))

            if len(dirty_players) > 0:
                ctx.broadcast_raw(encode_players(dirty_players), lambda lobby_conn: lobby_conn.authenticated)

            # TODO: This spams squillions of messages: we should implement per-connection message
            # aggregation at the next abstraction layer down :P
            for game in dirty_games:
                if game.state == GameState.ENDED:
                    game_service.remove_game(game)

                # So we're going to be broadcasting this to _somebody_...
                message = encode_dict(game.to_dict())

                # These games shouldn't be broadcast, but instead privately sent to those who are
                # allowed to see them.
                if game.visibility == VisibilityState.FRIENDS:
                    # To see this game, you must have an authenticated connection and be a friend of the host, or the host.
                    validation_func = lambda lobby_conn: lobby_conn.player.id in game.host.friends or lobby_conn.player == game.host
                else:
                    validation_func = lambda lobby_conn: lobby_conn.player.id not in game.host.foes

                ctx.broadcast_raw(message, lambda lobby_conn: lobby_conn.authenticated and validation_func(lobby_conn))
        except Exception as e:
            logging.getLogger().exception(e)
        finally:
            loop.call_later(DIRTY_REPORT_INTERVAL, report_dirties)

    ping_msg = encode_message('PING')

    def ping_broadcast():
        ctx.broadcast_raw(ping_msg)
        loop.call_later(45, ping_broadcast)

    def make_connection() -> LobbyConnection:
        return LobbyConnection(
            geoip=geoip_service,
            games=game_service,
            nts_client=nts_client,
            players=player_service,
            matchmaker_queue=matchmaker_queue
        )
    ctx = ServerContext(make_connection, name="LobbyServer")
    loop.call_later(DIRTY_REPORT_INTERVAL, report_dirties)
    loop.call_soon(ping_broadcast)
    loop.run_until_complete(ctx.listen(*address))
    return ctx
