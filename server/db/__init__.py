engine = None


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
    if port == 5432:
        from aiopg.sa import create_engine
    else:
        from aiomysql.sa import create_engine

    engine = await create_engine(
        host=host,
        port=port,
        user=user,
        password=password,
        db=db,
        autocommit=True,
        loop=loop,
        minsize=minsize,
        maxsize=maxsize,
        echo=echo
    )

    set_engine(engine)
    return engine
