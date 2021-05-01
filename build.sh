#!/usr/bin/env sh
pyinstaller unix.spec
cp ./install.sh ./dist/