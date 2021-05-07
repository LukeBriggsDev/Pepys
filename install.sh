#!/usr/bin/env sh
if test -f ~/.local/share/Pepys/resources/base/config.json; then
  rm ./Pepys/resources/base/config.json
fi
if test -f ~/.local/share/Pepys/resources/base/wordlist.txt; then
  rm ./Pepys/resources/base/wordlist.txt
fi
cp -r ./Pepys ~/.local/share/
printf "[Desktop Entry]\n \
Type=Application\n \
Name=Pepys\n \
Categories=Office;\n \
X-GNOME-FullName=Pepys\n \
Comment=A straightforward markdown journal\n \
Icon=%s/.local/share/Pepys/resources/base/icons/appicons/icon.svg\n \
NoDisplay=false\n \
Exec=%s/.local/share/Pepys/Pepys\n \
Path=\n \
Terminal=false\n \
X-GNOME-UsesNotifications=false\n \
StartupWMClass=Pepys" "$HOME" "$HOME" >> ~/.local/share/applications/Pepys.desktop