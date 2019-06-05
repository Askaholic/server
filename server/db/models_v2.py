from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        MetaData, SmallInteger, String, Table, Text)

metadata = MetaData()


email_domain_ban = Table(
    'email_domain_ban', metadata,
    Column('id', Integer, primary_key=True),
    Column('domain', String(255), nullable=False),
    Column('create_time', DateTime, nullable=False),
    Column('update_time', DateTime, nullable=False)
)

featured_mod = Table(
    'featured_mod', metadata,
    Column('id', Integer, primary_key=True),
    Column('short_name', String(50), nullable=False),
    Column('description', Text, nullable=False),
    Column('display_name', String(255), nullable=False),
    Column('public', Boolean, nullable=False),
    Column('ordinal', SmallInteger, nullable=False),
    Column('git_url', String(2000)),
    Column('git_branch', String(255)),
    Column('current_version', Integer, nullable=False),
    Column('deployment_webhook', Text),
    Column('allow_override', Boolean, nullable=False),
    Column('create_time', DateTime, nullable=False),
    Column('update_time', DateTime, nullable=False)
)

game = Table(
    'game', metadata,
    Column('id', Integer, primary_key=True),
    Column('start_time', DateTime, nullable=False),
    Column('end_time', DateTime),
    Column('featured_mod_id', ForeignKey('featured_mod.id'), nullable=False, index=True),
    Column('host_id', ForeignKey('account.id'), nullable=False),
    Column('map_version_id', ForeignKey('map_version.id'), nullable=False, index=True),
    Column('name', String(255), nullable=False),
    Column('validity', Enum('VALID', 'TOO_MANY_DESYNCS', 'WRONG_VICTORY_CONDITION', 'NO_FOG_OF_WAR', 'CHEATS_ENABLED', 'PREBUILT_ENABLED', 'NORUSH_ENABLED', 'BAD_UNIT_RESTRICTIONS', 'BAD_MAP', 'TOO_SHORT', 'BAD_MOD', 'COOP_NOT_RANKED', 'MUTUAL_DRAW', 'SINGLE_PLAYER', 'FFA_NOT_RANKED', 'UNEVEN_TEAMS_NOT_RANKED', 'UNKNOWN_RESULT', 'TEAMS_UNLOCKED', 'MULTIPLE_TEAMS', 'HAS_AI', 'STALE', 'SERVER_SHUTDOWN', name='game_validity'), nullable=False, index=True),
    Column('victory_condition', Enum('DEMORALIZATION', 'DOMINATION', 'ERADICATION', 'SANDBOX', name='victory_condition'), nullable=False),
    Column('create_time', DateTime, nullable=False),
    Column('update_time', DateTime, nullable=False)
)

leaderboard = Table(
    'leaderboard', metadata,
    Column('id', Integer, primary_key=True),
    Column('technical_name', String(255), nullable=False),
    Column('name_key', String(255), nullable=False),
    Column('description_key', String(255), nullable=False),
    Column('create_time', DateTime, nullable=False),
    Column('update_time', DateTime, nullable=False)
)

map_ = Table(
    'map', metadata,
    Column('id', Integer, primary_key=True),
    Column('display_name', String(100), nullable=False),
    Column('map_type', String(15), nullable=False),
    Column('battle_type', String(15), nullable=False),
    Column('uploader_id', ForeignKey('account.id')),
    Column('create_time', DateTime, nullable=False),
    Column('update_time', DateTime, nullable=False)
)

map_version = Table(
    'map_version', metadata,
    Column('id', Integer, primary_key=True),
    Column('description', Text),
    Column('max_players', SmallInteger, nullable=False),
    Column('width', SmallInteger, nullable=False),
    Column('height', SmallInteger, nullable=False),
    Column('version', SmallInteger, nullable=False),
    Column('filename', String(200), nullable=False),
    Column('ranked', Boolean, nullable=False),
    Column('hidden', Boolean, nullable=False),
    Column('map_id', ForeignKey('map.id'), nullable=False),
    Column('create_time', DateTime, nullable=False),
    Column('update_time', DateTime, nullable=False),
)

matchmaker_map = Table(
    'matchmaker_map', metadata,
    Column('id', Integer, primary_key=True),
    Column('map_version_id', ForeignKey('map_version.id')),
    Column('matchmaker_pool_id', ForeignKey('matchmaker_pool.id'), nullable=False),
    Column('create_time', DateTime, nullable=False),
    Column('update_time', DateTime, nullable=False)
)

matchmaker_pool = Table(
    'matchmaker_pool', metadata,
    Column('id', Integer, primary_key=True),
    Column('featured_mod_id', ForeignKey('featured_mod.id'), nullable=False),
    Column('leaderboard_id', ForeignKey('leaderboard.id'), nullable=False),
    Column('name_key', String(255), nullable=False),
    Column('create_time', DateTime, nullable=False),
    Column('update_time', DateTime, nullable=False),
    Column('technical_name', String(255), nullable=False, unique=True)
)

mod_version = Table(
    'mod_version', metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid', String, nullable=False, unique=True),
    Column('type', Enum('UI', 'SIM', name='mod_type'), nullable=False),
    Column('description', Text, nullable=False),
    Column('version', SmallInteger, nullable=False),
    Column('filename', String(255), nullable=False, unique=True),
    Column('icon', String(255)),
    Column('ranked', Boolean, nullable=False),
    Column('hidden', Boolean, nullable=False),
    Column('mod_id', ForeignKey('mod.id'), nullable=False),
    Column('create_time', DateTime, nullable=False),
    Column('update_time', DateTime, nullable=False),
)
