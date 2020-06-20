from datetime import datetime, timedelta

import mock
import pytest

from server.matchmaker import MatchOffer, OfferTimeoutError
from tests.utils import fast_forward


@pytest.fixture
def offer(player_factory):
    return MatchOffer(
            [player_factory(player_id=i) for i in range(5)],
            datetime(2020, 1, 31, 14, 30, 36)
        )


def test_match_offer_api(offer):

    assert offer.to_dict() == {
        "expires_at": "2020-01-31T14:30:36",
        "players_total": 5,
        "players_ready": 0
    }

    assert len(list(offer.get_ready_players())) == 0
    assert len(list(offer.get_unready_players())) == 5


def test_broadcast_called_on_ready(offer):
    offer.write_broadcast_update = mock.Mock()
    player = next(offer.get_unready_players())

    offer.ready_player(player)

    offer.write_broadcast_update.assert_called_once()


def test_ready_player_bad_key(offer, player_factory):
    with pytest.raises(KeyError):
        offer.ready_player(player_factory(player_id=42))


@pytest.mark.asyncio
async def test_wait_ready_timeout(offer):
    with pytest.raises(OfferTimeoutError):
        await offer.wait_ready()


@pytest.mark.asyncio
@fast_forward(5)
async def test_wait_ready_timeout_some_ready(offer):
    offer.expires_at = datetime.now() + timedelta(seconds=5)

    players = offer.get_unready_players()
    p1, p2 = next(players), next(players)

    offer.ready_player(p1)
    offer.ready_player(p2)

    with pytest.raises(OfferTimeoutError):
        await offer.wait_ready()


@pytest.mark.asyncio
async def test_wait_ready(offer):
    offer.expires_at = datetime.now() + timedelta(seconds=5)

    for player in offer.get_unready_players():
        offer.ready_player(player)

    await offer.wait_ready()
