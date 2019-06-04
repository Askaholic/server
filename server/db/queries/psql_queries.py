async def select_coop_maps(conn):
    raise NotImplementedError()


async def delete_social(conn, user_id, subject_id):
    raise NotImplementedError()


async def insert_social(conn, user_id, subject_id, status):
    raise NotImplementedError()


async def select_lobby_ban(conn, user_id):
    raise NotImplementedError()


async def insert_lobby_ban(
    conn, player_id, author_id, reason, period, duration="DAY", level='GLOBAL'
):
    raise NotImplementedError()


async def select_avatars_list(conn):
    raise NotImplementedError()


async def delete_avatar(conn, user_id, avatar_id):
    raise NotImplementedError()
