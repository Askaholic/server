"""
Call `connect_engine` in order to initialize these module variables:
    * engine
    * queries
"""
engine = None
queries = None


def set_engine(engine_):
    """
    Set the globally used engine to the given argument
    """
    global engine
    engine = engine_


async def connect_engine(
    loop, host='localhost', port=3306, user='root', password='', db='faf_test',
    minsize=1, maxsize=1, echo=True
):
    global queries
    if int(port) == 5432:
        from aiopg.sa import create_engine
        from .queries import psql_queries
        queries = psql_queries
        kwargs = {
            "database": db
        }
    else:
        from aiomysql.sa import create_engine
        from .queries import mysql_queries
        queries = mysql_queries
        kwargs = {
            "db": db,
            "autocommit": True
        }

    engine = await create_engine(
        loop=loop,
        host=host,
        port=port,
        user=user,
        password=password,
        minsize=minsize,
        maxsize=maxsize,
        echo=echo,
        **kwargs
    )

    set_engine(engine)
    return engine
