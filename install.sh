#!/usr/bin/env sh
cp -r ./Pepys ~/.local/share/
printf "[Desktop Entry]\n \
Type=Application\n \
Name=Pepys\n \
Categories=Office;\n \
X-GNOME-FullName[en_GB.UTF-8]=Pepys\n \
Comment[en_GB.UTF-8]=A straightforward markdown journal\n \
Icon=%s/.local/share/Pepys/resources/base/icons/appicons/icon.svg\n \
NoDisplay=false\n \
Exec=%s/.local/share/Pepys/Pepys\n \
Path=\n \
Terminal=false\n \
X-GNOME-UsesNotifications=false\n \
StartupWMClass=Pepys" "$HOME" "$HOME" >> ~/.local/share/applications/Pepys.desktop