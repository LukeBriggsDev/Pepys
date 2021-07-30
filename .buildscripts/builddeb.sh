#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PACKAGE_NAME="pepys_1.0.9-1"
mkdir -p $SCRIPT_DIR/../deb_build/$PACKAGE_NAME/usr/share/pepys/
mkdir -p $SCRIPT_DIR/../deb_build/$PACKAGE_NAME/usr/bin
mkdir -p $SCRIPT_DIR/../deb_build/$PACKAGE_NAME/DEBIAN
rm -r $SCRIPT_DIR/../deb_build/$PACKAGE_NAME/usr/share/pepys/*
cp -r $SCRIPT_DIR/../src $SCRIPT_DIR/../deb_build/$PACKAGE_NAME/usr/share/pepys
# control script
echo "Package: pepys
Version: 1.0.9-1
Section: base
Priority: optional
Architecture: all
Depends: python3, python3-wheel, python3-pip, python3-pypdf2, pandoc, enchant, wkhtmltopdf, python3-pyqt5, python3-pyqt5.qtwebengine, python3-regex, python3-num2words, python3-pypandoc, python3-enchant, python3-setproctitle, python3-yaml
Maintainer: Luke Briggs <lukebriggs02@gmail.com>
Description: A straightforward markdown journal
" > $SCRIPT_DIR/../deb_build/$PACKAGE_NAME/DEBIAN/control

# bin exec
echo "#!/usr/bin/env sh
python3 /usr/share/pepys/src/main/python/main.py" > $SCRIPT_DIR/../deb_build/$PACKAGE_NAME/usr/bin/pepys

# desktop file
mkdir -p $SCRIPT_DIR/../deb_build/$PACKAGE_NAME/usr/local/share/applications
echo "[Desktop Entry]
Type=Application
Name=Pepys
Categories=Office;
X-GNOME-FullName=Pepys
Comment=A straightforward markdown journal
Icon=dev.lukebriggs.pepys
NoDisplay=false
Exec=runner.sh
Path=
Terminal=false
X-GNOME-UsesNotifications=false
StartupWMClass=Pepys" > $SCRIPT_DIR/../deb_build/$PACKAGE_NAME/usr/local/share/applications/pepys.desktop

dpkg-deb --build $SCRIPT_DIR/../deb_build/$PACKAGE_NAME

