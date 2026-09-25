#!/usr/bin/env bash

set -eux

sqlite3 gaps.db "select discoverer,count(*) from gaps WHERE discoverer not in (select abbreviation from credits) GROUP BY 1 ORDER BY 2 DESC"
