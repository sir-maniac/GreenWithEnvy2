#!/usr/bin/env bash


flatpak uninstall io.github.sir_maniac.gwe2 -y
./build.sh -fl -fb -fi
flatpak run io.github.sir_maniac.gwe2 --debug
