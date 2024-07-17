#!/bin/bash
#
# insta485db

set -Eeuo pipefail
set -x

pycodestyle insta485
pydocstyle insta485
pylint --disable=cyclic-import insta485
