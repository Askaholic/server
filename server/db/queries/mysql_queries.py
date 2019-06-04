from sqlalchemy import and_, func, text

from ..models import ban, friends_and_foes


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
    conn, player_id, author_id, reason, period, duration="DAY", level='GLOBAL'
):
    await conn.execute(
        ban.insert().values(
            player_id=player_id,
            author_id=author_id,
            reason=reason,
            expires_at=func.date_add(
                func.now(), text(f"interval :duration {period}")
            ),
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
