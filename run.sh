#!/usr/bin/env bash

# ensure we are at project root
cd -P "$(dirname "${BASH_SOURCE[0]}")"

. build.sh && \
ninja -v -C ${MESON_BUILD_DIR} debug
