#!/bin/bash

set -e

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
LIB_DIR="$( cd "$( pwd )/../lib" && pwd )"

coverage run "--omit=$LIB_DIR/*,/usr/*" bark/auth/tests.py
coverage html
