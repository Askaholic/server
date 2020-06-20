import asyncio
from datetime import datetime
from typing import Generator, Iterable

from ..players import Player


class OfferTimeoutError(asyncio.TimeoutError):
    pass


class MatchOffer(object):
    """
    Track which players are ready for a match to begin.

    Once a player has become ready, they cannot become unready again. State
    changes are eagerly broadcast to other players in the MatchOffer.
    """

    def __init__(self, players: Iterable[Player], expires_at: datetime):
        self.expires_at = expires_at
        self._players_ready = {player: False for player in players}
        self.future = asyncio.Future()

    def get_unready_players(self) -> Generator[Player, None, None]:
        return (
            player for player, ready in self._players_ready.items()
            if not ready
        )

    def get_ready_players(self) -> Generator[Player, None, None]:
        return (
            player for player, ready in self._players_ready.items()
            if ready
        )

    def ready_player(self, player: Player) -> None:
        """
        Mark a player as ready.

        Broadcasts the state change to other players.
        """
        if self._players_ready[player]:
            # This client's state is probably out of date
            player.write_message({
                "command": "match_info",
                **self.to_dict(),
                "ready": True
            })
        else:
            self._players_ready[player] = True
            self.write_broadcast_update()

        if all(self._players_ready.values()) and not self.future.done():
            self.future.set_result(True)

    async def wait_ready(self) -> None:
        """Wait for all players to have readied up."""
        timeout = (self.expires_at - datetime.now()).total_seconds()
        if timeout <= 0:
            raise OfferTimeoutError()

        try:
            await asyncio.wait_for(self.future, timeout=timeout)
        except asyncio.TimeoutError:
            raise OfferTimeoutError()

    def write_broadcast_update(self) -> None:
        """Queue the `match_info` message to be sent to all players in the
        MatchOffer."""
        info = self.to_dict()
        for player, ready in self._players_ready.items():
            player.write_message({
                "command": "match_info",
                **info,
                "ready": ready
            })

    def to_dict(self) -> dict:
        return {
            "expires_at": self.expires_at.isoformat(),
            "players_total": len(self._players_ready),
            # Works because `True` is counted as 1 and `False` as 0
            "players_ready": sum(self._players_ready.values())
        }
