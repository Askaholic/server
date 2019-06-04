"""
Implementation of database queries. Note that modules mysql_queries
and psql_queries must have the SAME interface.
"""

from . import mysql_queries, psql_queries
import inspect

# Verify that module interfaces are the same


def is_pub_member(x):
    if not inspect.isfunction(x) or not x.__module__.startswith(__name__):
        return False


def public_api(module):
    return set(
        map(
            lambda x: inspect.signature(x[1]),
            inspect.getmembers(module, is_pub_member)
        )
    )


assert public_api(mysql_queries) == public_api(psql_queries), \
    "MySQL and PSQL queries don't implement the same functionality!"

__all__ = [
    'mysql_queries',
    'psql_queries',
]
