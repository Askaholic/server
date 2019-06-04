from sqlalchemy import and_, func, select, text

from ..models import (
    avatars, avatars_list, ban, clan, clan_membership, friends_and_foes,
    game_featuredMods, game_player_stats, game_stats, global_rating,
    ladder1v1_rating, login
)


async def select_coop_maps(conn):
    return await conn.execute(
        "SELECT name, description, filename, type, id FROM `coop_map`"
    )


async def select_coop_map_id(conn, filename):
    return await conn.execute(
        "SELECT `id` FROM `coop_map` WHERE `filename` = %s", filename
    )


async def delete_social(conn, user_id, subject_id):
    await conn.execute(
        friends_and_foes.delete().where(
            and_(
                friends_and_foes.c.user_id == user_id,
                friends_and_foes.c.subject_id == subject_id
            )
        )
    )


async def insert_social(conn, user_id, subject_id, status):
    await conn.execute(
        friends_and_foes.insert().values(
            user_id=user_id, subject_id=subject_id, status=status
        )
    )


async def select_lobby_ban(conn, user_id):
    return await conn.execute(
        "SELECT reason from lobby_ban WHERE idUser=%s AND expires_at > NOW()",
        user_id
    )


async def insert_lobby_ban(
    conn,
    player_id,
    author_id,
    reason,
    period=None,
    duration="DAY",
    level='GLOBAL'
):
    await conn.execute(
        ban.insert().values(
            player_id=player_id,
            author_id=author_id,
            reason=reason,
            expires_at=func.date_add(
                func.now(), text(f"interval :duration {period}")
            ) if period is not None else None,
            level=level
        ),
        duration=duration
    )


async def select_avatars_list(conn):
    return await conn.execute("SELECT url, tooltip FROM `avatars_list`")


async def delete_avatar(conn, user_id, avatar_id):
    await conn.execute(
        "DELETE FROM `avatars` "
        "WHERE `idUser` = %s "
        "AND `idAvatar` = %s", (user_id, avatar_id)
    )


async def delete_user_avatars(conn, username):
    await conn.execute(
        "DELETE FROM `avatars` "
        "WHERE `idUser` = "
        "(SELECT `id` FROM `login` WHERE `login`.`login` = %s)", username
    )


async def insert_user_avatar(conn, username, avatar):
    await conn.execute(
        "INSERT INTO `avatars`(`idUser`, `idAvatar`) "
        "VALUES ((SELECT id FROM login WHERE login.login = %s),"
        "(SELECT id FROM avatars_list WHERE avatars_list.url = %s)) "
        "ON DUPLICATE KEY UPDATE `idAvatar` = (SELECT id FROM avatars_list WHERE avatars_list.url = %s)",
        (username, avatar, avatar)
    )


async def select_login_info(conn, username):
    return await conn.execute(
        "SELECT login.id as id,"
        "login.login as username,"
        "login.password as password,"
        "login.steamid as steamid,"
        "login.create_time as create_time,"
        "lobby_ban.reason as reason,"
        "lobby_ban.expires_at as expires_at "
        "FROM login "
        "LEFT JOIN lobby_ban ON login.id = lobby_ban.idUser "
        "WHERE LOWER(login)=%s "
        "ORDER BY expires_at DESC", username
    )


async def update_login(conn, ip, user_agent, player_id):
    await conn.execute(
        "UPDATE login SET ip = %(ip)s, user_agent = %(user_agent)s, last_login = NOW() WHERE id = %(player_id)s",
        {
            "ip": ip,
            "user_agent": user_agent,
            "player_id": player_id
        }
    )


async def update_irc_login(conn, username, password):
    await conn.execute(
        "UPDATE anope.anope_db_NickCore SET pass = %s WHERE display = %s",
        (password, username)
    )


async def select_social(conn, player_id):
    return await conn.execute(
        "SELECT `subject_id`, `status` "
        "FROM friends_and_foes WHERE user_id = %s", player_id
    )


async def select_user_avatars(conn, player_id):
    return await conn.execute(
        "SELECT url, tooltip FROM `avatars` "
        "LEFT JOIN `avatars_list` ON `idAvatar` = `avatars_list`.`id` WHERE `idUser` = %s",
        player_id
    )


async def update_user_avatars_deselect_all(conn, player_id):
    await conn.execute(
        "UPDATE `avatars` SET `selected` = 0 WHERE `idUser` = %s", player_id
    )


async def update_user_avatars_set_selected(conn, player_id, avatar):
    await conn.execute(
        "UPDATE `avatars` SET `selected` = 1 WHERE `idAvatar` ="
        "(SELECT id FROM avatars_list WHERE avatars_list.url = %s) and "
        "`idUser` = %s", (avatar, player_id)
    )


async def select_matchmaker_ban(conn, player_id):
    return await conn.execute(
        "SELECT id FROM matchmaker_ban WHERE `userid` = %s", player_id
    )


async def select_mods(conn):
    return await conn.execute(
        "SELECT uid, name, version, author, ui, date, downloads, likes, played, description, filename, icon FROM table_mod ORDER BY likes DESC LIMIT 100"
    )


async def select_mods_in(conn, uids):
    return await conn.execute(
        text("SELECT `uid`, `name` from `table_mod` WHERE `uid` in :ids"),
        ids=tuple(uids)
    )


async def select_mod(conn, uid):
    return await conn.execute(
        "SELECT uid, name, version, author, ui, date, downloads, likes, played, description, filename, icon, likers FROM `table_mod` WHERE uid = %s LIMIT 1",
        uid
    )


async def update_liked_mod(conn, uid, likers):
    await conn.execute(
        "UPDATE mod_stats s "
        "JOIN mod_version v ON v.mod_id = s.mod_id "
        "SET s.likes = s.likes + 1, likers=%s WHERE v.uid = %s", likers, uid
    )


async def update_downloaded_mod(conn, uid):
    await conn.execute(
        "UPDATE mod_stats s "
        "JOIN mod_version v ON v.mod_id = s.mod_id "
        "SET downloads=downloads+1 WHERE v.uid = %s", uid
    )


async def update_played_mods(conn, uids):
    await conn.execute(
        text(
            """ UPDATE mod_stats s JOIN mod_version v ON v.mod_id = s.mod_id
            SET s.times_played = s.times_played + 1 WHERE v.uid in :ids"""
        ),
        ids=tuple(uids)
    )


async def select_player_data(conn, player_id):
    # yapf: disable
    sql = select(
        [
            avatars_list.c.url,
            avatars_list.c.tooltip,
            global_rating.c.mean,
            global_rating.c.deviation,
            global_rating.c.numGames,
            ladder1v1_rating.c.mean,
            ladder1v1_rating.c.deviation,
            clan.c.tag,
        ],
        use_labels=True,
    ).select_from(
        login.join(global_rating)
        .join(ladder1v1_rating)
        .outerjoin(clan_membership)
        .outerjoin(clan)
        .outerjoin(avatars)
        .outerjoin(avatars_list)
    ).where(login.c.id == player_id)
    # yapf: enable

    return await conn.execute(sql)


async def select_lobby_admins(conn):
    return await conn.execute("SELECT `user_id`, `group` FROM lobby_admin")


async def select_uniqueid_exempt(conn):
    return await conn.execute("SELECT `user_id` FROM uniqueid_exempt")


async def select_client_version(conn):
    return await conn.execute(
        "SELECT version, file FROM version_lobby ORDER BY id DESC LIMIT 1"
    )


async def select_email_blacklist(conn):
    return await conn.execute("SELECT domain FROM email_domain_blacklist")


async def select_ladder_history(conn, player_id, limit):
    query = select([
        game_stats.c.mapId,
    ]).select_from(
        game_player_stats.join(game_stats).join(game_featuredMods)
    ).where(
        and_(
            game_player_stats.c.playerId == player_id,
            game_stats.c.startTime >= func.now() - text("interval 1 day"),
            game_featuredMods.c.gamemod == "ladder1v1"
        )
    ).order_by(game_stats.c.startTime.desc()).limit(limit)
    return await conn.execute(query)


async def select_game_counter(conn):
    # InnoDB, unusually, doesn't allow insertion of values greater than the next expected
    # value into an auto_increment field. We'd like to do that, because we no longer insert
    # games into the database when they don't start, so game ids aren't contiguous (as
    # unstarted games consume ids that never get written out).
    # So, id has to just be an integer primary key, no auto-increment: we handle its
    # incrementing here in game service, but have to do this slightly expensive query on
    # startup (though the primary key index probably makes it super fast anyway).
    # This is definitely a better choice than inserting useless rows when games are created,
    # doing LAST_UPDATE_ID to get the id number, and then doing an UPDATE when the actual
    # data to go into the row becomes available: we now only do a single insert for each
    # game, and don't end up with 800,000 junk rows in the database.
    return await conn.execute("SELECT MAX(id) FROM game_stats")


async def select_featured_mods(conn):
    return await conn.execute(
        "SELECT `id`, `gamemod`, `name`, description, publish, `order` FROM game_featuredMods"
    )


async def select_ranked_mod_ids(conn):
    return await conn.execute("SELECT uid FROM table_mod WHERE ranked = 1")


async def select_ladder_map_pool(conn):
    return await conn.execute(
        "SELECT ladder_map.idmap, "
        "table_map.name, "
        "table_map.filename "
        "FROM ladder_map "
        "INNER JOIN table_map ON table_map.id = ladder_map.idmap"
    )


async def select_featured_mod_info(conn, mod_name):
    t = f"updates_{mod_name}"
    tfiles = f"{t}_files"
    return await conn.execute(
        f"SELECT {tfiles}.fileId, MAX({tfiles}.version) "
        f"FROM {tfiles} LEFT JOIN {t} ON {tfiles}.fileId = {t}.id "
        f"GROUP BY {tfiles}.fileId"
    )


async def insert_coop_leaderboard_entry(
    conn, mission, gameuid, secondary, delta, player_count
):
    await conn.execute(
        """ INSERT INTO `coop_leaderboard`
            (`mission`, `gameuid`, `secondary`, `time`, `player_count`)
            VALUES (%s, %s, %s, %s, %s)""",
        (mission, gameuid, secondary, delta, player_count)
    )


async def insert_teamkill_report(
    conn, teamkiller_id, victim_id, gameuid, gametime
):
    await conn.execute(
        """ INSERT INTO `teamkills` (`teamkiller`, `victim`, `game_id`, `gametime`)
            VALUES (%s, %s, %s, %s)""",
        (teamkiller_id, victim_id, gameuid, gametime)
    )


async def update_game_ended(conn, gameuid):
    await conn.execute(
        "UPDATE game_stats "
        "SET endTime = NOW() "
        "WHERE id = %s", gameuid
    )


async def select_game_player_stats(conn, gameuid):
    return await conn.execute(
        "SELECT `playerId`, `place`, `score` "
        "FROM `game_player_stats` "
        "WHERE `gameId`=%s", gameuid
    )


async def update_game_scores(conn, rows):
    await conn.execute(
        "UPDATE game_player_stats "
        "SET `score`=%s, `scoreTime`=NOW() "
        "WHERE `gameId`=%s AND `playerId`=%s", rows
    )


async def delete_game_stats(conn, gameuid):
    await conn.execute(
        "DELETE FROM game_player_stats "
        "WHERE gameId=%s", gameuid
    )
    await conn.execute("DELETE FROM game_stats WHERE id=%s", gameuid)


async def update_game_ratings(conn, mean, deviation, gameuid, player_id):
    await conn.execute(
        "UPDATE game_player_stats "
        "SET after_mean = %s, after_deviation = %s, scoreTime = NOW() "
        "WHERE gameId = %s AND playerId = %s",
        (mean, deviation, gameuid, player_id)
    )


async def update_rating(conn, rating, player_id, mean, deviation, is_victory):
    table = {"ladder": "ladder1v1_rating", "global": "global_rating"}[rating]
    # If we are updating the ladder1v1_rating table then we also need to update
    # the `winGames` column which doesn't exist on the global_rating table
    if table == 'ladder1v1_rating':
        await conn.execute(
            "UPDATE ladder1v1_rating "
            "SET mean = %s, is_active=1, deviation = %s, numGames = numGames + 1, winGames = winGames + %s "
            "WHERE id = %s",
            (mean, deviation, 1 if is_victory else 0, player_id)
        )
    else:
        await conn.execute(
            "UPDATE " + table + " "
            "SET mean = %s, is_active=1, deviation = %s, numGames = numGames + 1 "
            "WHERE id = %s", (mean, deviation, player_id)
        )


async def select_map(conn, map_file_path):
    return await conn.execute(
        "SELECT id, ranked FROM map_version "
        "WHERE lower(filename) = lower(%s)", map_file_path
    )


async def insert_game_stats(
    conn, gameuid, game_type, mod_uid, host_id, map_id, name, validity
):
    await conn.execute(
        "INSERT INTO game_stats(id, gameType, gameMod, `host`, mapId, gameName, validity)"
        "VALUES(%s, %s, %s, %s, %s, %s, %s)",
        (gameuid, game_type, mod_uid, host_id, map_id, name, validity)
    )


async def insert_game_player_stats(conn, query_args):
    await conn.execute(
        "INSERT INTO `game_player_stats` "
        "(`gameId`, `playerId`, `faction`, `color`, `team`, `place`, `mean`, `deviation`, `AI`, `score`) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", query_args
    )


async def update_invalid_game(conn, gameuid, validity):
    await conn.execute(
        "UPDATE game_stats SET validity = %s "
        "WHERE id = %s", (validity, gameuid)
    )
