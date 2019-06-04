async def select_coop_maps(conn):
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


async def select_mod(conn, uid):
    raise NotImplementedError()


async def update_liked_mod(conn, uid, likers):
    raise NotImplementedError()


async def update_downloaded_mod(conn, uid):
    raise NotImplementedError()


async def select_player_data(conn, player_id):
    raise NotImplementedError()


async def select_lobby_admins(conn):
    raise NotImplementedError()


async def select_uniqueid_exempt(conn):
    raise NotImplementedError()


async def select_client_version(conn):
    raise NotImplementedError()


async def select_email_blacklist(conn):
    raise NotImplementedError()
