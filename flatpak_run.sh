#!/usr/bin/env bash

# ensure we are at project root
cd -P "$(dirname "${BASH_SOURCE[0]}")"

flatpak uninstall io.github.sir_maniac.gwe2 -y
./build.sh -fl -fb -fi
flatpak run io.github.sir_maniac.gwe2 --debug
