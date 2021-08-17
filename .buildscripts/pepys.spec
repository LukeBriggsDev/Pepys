Name:           Pepys
Version:        1.1.1
Release:        1%{?dist}
Summary:        A straightforward markdown journal

License:        GPLv3
URL:            https://www.lukebriggs.dev/pepys
Source0:        pepys.tar.gz

Requires:       python3, python3-wheel, python3-pip, python3-PyPDF2, pandoc, enchant, wkhtmltopdf, python3-qt5, python3-qt5-webengine, python3-regex, python3-num2words, python3-pypandoc, python3-enchant, python3-setproctitle, python3-pyyaml
%description

%build
MAIN_DIR=%{buildroot}/usr/share/pepys
APP_DIR=%{buildroot}/usr/local/share/applications
mkdir -p ${MAIN_DIR}/temp
mkdir -p ${APP_DIR}
tar -xzvf %{SOURCE0} -C ${MAIN_DIR}/temp
cp -r ${MAIN_DIR}/temp/* ${MAIN_DIR}
rm -rf ${MAIN_DIR}/temp
echo "[Desktop Entry]
Type=Application
Name=Pepys
Categories=Office;
X-GNOME-FullName=Pepys
Comment=A straightforward markdown journal
Icon=/usr/share/pepys/src/main/resources/base/icons/appicons/icon.svg
NoDisplay=false
Exec=pepys
Path=
Terminal=false
X-GNOME-UsesNotifications=false
StartupWMClass=Pepys" > $APP_DIR/pepys.desktop

%files
/*

%post
echo "#!/usr/bin/env sh
python3 /usr/share/pepys/src/main/python/main.py" > /usr/bin/pepys
chmod +x /usr/bin/pepys

#%license add-license-file-here
#%doc add-docs-here



%changelog
* Sat May 15 2021 Luke Briggs <lukebriggs02@gmail.com>
- Not Much