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
    raise NotImplementedError()


async def select_lobby_admins(conn):
    raise NotImplementedError()


async def select_uniqueid_exempt(conn):
    raise NotImplementedError()


async def select_client_version(conn):
    raise NotImplementedError()


async def select_email_blacklist(conn):
    raise NotImplementedError()


async def select_ladder_history(conn, player_id, limit):
    raise NotImplementedError()


async def select_game_counter(conn):
    raise NotImplementedError()


async def select_featured_mods(conn):
    raise NotImplementedError()


async def select_ranked_mod_ids(conn):
    raise NotImplementedError()


async def select_ladder_map_pool(conn):
    raise NotImplementedError()


async def select_featured_mod_info(conn, mod_name):
    raise NotImplementedError()


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
