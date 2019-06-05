#!/usr/bin/env bash
set -e
# py.test --cov-report term-missing --cov=server --mysql_database=faf
py.test --cov-report term-missing --cov=server --mysql_database=sh --mysql_username=postgres --mysql_password=apple --mysql_port=5432 -s
