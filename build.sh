#!/usr/bin/env sh
if command -v pyinstaller; then
  pyinstaller unix.spec
elif [ -n "$(find ./ -type f -iname pyinstaller)" ]; then
  eval "$(find ./ -type f -iname pyinstaller) unix.spec";
else
  echo "No pyinstaller detected";
  exit 1;
fi
cp ./install.sh ./dist/