from sqlalchemy import func, select, and_

from ..models_v2 import (
    account, avatar, avatar_assignment, clan, clan_membership,
    email_domain_ban, featured_mod, game, leaderboard, leaderboard_rating,
    map_, map_version, matchmaker_map, matchmaker_pool, mod_version
)


class EmptyResultProxy(object):
    """ Use this to return empty results without performing a query"""

    async def fetchall(self):
        return []

    async def fetchone(self):
        return None


async def select_coop_maps(conn):
    raise NotImplementedError()


async def select_coop_map_id(conn, filename):
    raise NotImplementedError()


async def delete_social(conn, user_id, subject_id):
    raise NotImplementedError()


async def insert_social(conn, user_id, subject_id, status):
    raise NotImplementedError()


async def select_lobby_ban(conn, user_id):
    raise NotImplementedError()


async def insert_lobby_ban(
    conn,
    player_id,
    author_id,
    reason,
    period=None,
    duration="DAY",
    level='GLOBAL'
):
    raise NotImplementedError()


async def select_avatars_list(conn):
    raise NotImplementedError()


async def delete_avatar(conn, user_id, avatar_id):
    raise NotImplementedError()


async def delete_user_avatars(conn, username):
    raise NotImplementedError()


async def insert_user_avatar(conn, username, avatar):
    raise NotImplementedError()


async def select_login_info(conn, username):
    raise NotImplementedError()


async def update_login(conn, ip, user_agent, player_id):
    raise NotImplementedError()


async def update_irc_login(conn, username, password):
    raise NotImplementedError()


async def select_social(conn, player_id):
    raise NotImplementedError()


async def select_user_avatars(conn, player_id):
    raise NotImplementedError()


async def update_user_avatars_deselect_all(conn, player_id):
    raise NotImplementedError()


async def update_user_avatars_set_selected(conn, player_id, avatar):
    raise NotImplementedError()


async def select_matchmaker_ban(conn, player_id):
    raise NotImplementedError()


async def select_mods(conn):
    raise NotImplementedError()


async def select_mods_in(conn, uids):
    raise NotImplementedError()


async def select_mod(conn, uid):
    raise NotImplementedError()


async def update_liked_mod(conn, uid, likers):
    raise NotImplementedError()


async def update_downloaded_mod(conn, uid):
    raise NotImplementedError()


async def update_played_mods(conn, uids):
    raise NotImplementedError()


async def select_player_data(conn, player_id):
    # yapf: disable

    # TODO: Refactor this and add permissions
    sql = select(
        [
            avatar.c.url.label("avatar_url"),
            avatar.c.description.label("avatar_tooltip"),
            select([leaderboard_rating.c.mean]).select_from(
                leaderboard_rating.join(leaderboard)
            ).where(and_(
                leaderboard.c.technical_name == "global",
                leaderboard_rating.c.account_id == account.c.id
            )).label("global_mean"),
            select([leaderboard_rating.c.deviation]).select_from(
                leaderboard_rating.join(leaderboard)
            ).where(and_(
                leaderboard.c.technical_name == "global",
                leaderboard_rating.c.account_id == account.c.id
            )).label("global_deviation"),
            select([leaderboard_rating.c.total_games]).select_from(
                leaderboard_rating.join(leaderboard)
            ).where(and_(
                leaderboard.c.technical_name == "global",
                leaderboard_rating.c.account_id == account.c.id
            )).label("global_num_games"),
            select([leaderboard_rating.c.mean]).select_from(
                leaderboard_rating.join(leaderboard)
            ).where(and_(
                leaderboard.c.technical_name == "ladder1v1",
                leaderboard_rating.c.account_id == account.c.id
            )).label("ladder_mean"),
            select([leaderboard_rating.c.deviation]).select_from(
                leaderboard_rating.join(leaderboard)
            ).where(and_(
                leaderboard.c.technical_name == "ladder1v1",
                leaderboard_rating.c.account_id == account.c.id
            )).label("ladder_deviation"),
            clan.c.tag.label("clan_tag"),
        ],
    ).select_from(
        account
        .outerjoin(clan_membership)
        .outerjoin(clan)
        .outerjoin(avatar_assignment)
        .outerjoin(avatar)
    ).where(account.c.id == player_id)
    # yapf: enable

    return await conn.execute(sql)


async def select_uniqueid_exempt(conn):
    return EmptyResultProxy()


async def select_client_version(conn):
    return EmptyResultProxy()


async def select_email_blacklist(conn):
    return await conn.execute(select([email_domain_ban.c.domain]))


async def select_ladder_history(conn, player_id, limit):
    raise NotImplementedError()


async def select_game_counter(conn):
    return await conn.execute(select([func.max(game.c.id)]))


async def select_featured_mods(conn):
    return await conn.execute(
        select([
            featured_mod.c.id,
            featured_mod.c.short_name,
            featured_mod.c.display_name,
            featured_mod.c.description,
            featured_mod.c.public,
            featured_mod.c.ordinal,
        ])
    )


async def select_ranked_mod_ids(conn):
    # yapf: disable
    return await conn.execute(
        select([mod_version.c.uuid])
        .where(mod_version.c.ranked is True)
    )
    # yapf: enable


async def select_ladder_map_pool(conn):
    # yapf: disable
    return await conn.execute(
        select([
            matchmaker_map.c.map_version_id,
            map_.c.display_name,
            map_version.c.filename,
        ]).select_from(
            matchmaker_pool
            .join(leaderboard)
            .join(matchmaker_map)
            .join(map_version)
            .join(map_)
        ).where(leaderboard.c.technical_name == 'ladder1v1')
    )


async def select_featured_mod_info(conn, mod_name):
    return await conn.execute(
        select([0, featured_mod.c.current_version])
        .where(featured_mod.c.short_name == mod_name)
    )
    # yapf: enable


async def insert_coop_leaderboard_entry(
    conn, mission, gameuid, secondary, delta, player_count
):
    raise NotImplementedError()


async def insert_teamkill_report(
    conn, teamkiller_id, victim_id, gameuid, gametime
):
    raise NotImplementedError()


async def update_game_ended(conn, gameuid):
    raise NotImplementedError()


async def select_game_player_stats(conn, gameuid):
    raise NotImplementedError()


async def update_game_scores(conn, rows):
    raise NotImplementedError()


async def delete_game_stats(conn, gameuid):
    raise NotImplementedError()


async def update_game_ratings(conn, mean, deviation, gameuid, player_id):
    raise NotImplementedError()


async def update_rating(conn, rating, player_id, mean, deviation, is_victory):
    raise NotImplementedError()


async def select_map(conn, map_file_path):
    raise NotImplementedError()


async def insert_game_stats(
    conn, gameuid, game_type, mod_uid, host_id, map_id, name, validity
):
    raise NotImplementedError()


async def insert_game_player_stats(conn, query_args):
    raise NotImplementedError()


async def update_invalid_game(conn, gameuid, validity):
    raise NotImplementedError()
