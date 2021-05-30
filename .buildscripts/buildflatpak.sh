#!/usr/bin/env sh
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
mkdir -p $SCRIPT_DIR/../.flatpak_build
mkdir -p $SCRIPT_DIR/../.flatpak_sources
tar -C $SCRIPT_DIR/../ -czvf $SCRIPT_DIR/../.flatpak_sources/src.tar.gz src
flatpak-builder --force-clean $SCRIPT_DIR/../.flatpak_build $SCRIPT_DIR/../dev.lukebriggs.pepys.yml
