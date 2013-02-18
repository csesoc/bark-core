#!/bin/bash

set -e

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
LIB_DIR="$( cd "$( pwd )/../lib" && pwd )"

coverage run --source=bark bark/auth/tests.py
coverage run --source=bark --append bark/swipe/tests.py
coverage html
