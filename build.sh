#!/usr/bin/env sh
if command -v pyinstaller; then
  pyinstaller unix.spec
elif ! [ -n "$(find ./ -type f -iname pyinstaller)" ]; then
  find ./ -type f -iname pyinstaller -exec {} \;
else
  echo "No pyinstaller detected";
  exit 1;
fi
cp ./install.sh ./dist/