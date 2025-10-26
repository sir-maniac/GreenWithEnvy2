#!/usr/bin/env bash

# ensure we are at project root
cd -P "$(dirname "${BASH_SOURCE[0]}")"

. build.sh && \
bin/run-local.py
