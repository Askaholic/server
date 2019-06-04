from sqlalchemy import and_, func, select, text

from ..models import (
    avatars, avatars_list, ban, clan, clan_membership, friends_and_foes,
    global_rating, ladder1v1_rating, login
)


async def select_coop_maps(conn):
    return await conn.execute(
        "SELECT name, description, filename, type, id FROM `coop_map`"
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
