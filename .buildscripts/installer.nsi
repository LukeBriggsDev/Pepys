Outfile "pepys_install.exe"
InstallDir "$PROGRAMFILES64\Pepys"
Section "Install"
    SetOutPath "$INSTDIR"
    File /r src
    File /r venv
    File Pepys.exe
    inetc::get "https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6-1.mxe-cross-win64.7z" "$INSTDIR\wkhtmltox.7z"
    Nsis7z::Extract "$INSTDIR\wkhtmltox.7z"
    inetc::get "https://github.com/jgm/pandoc/releases/download/2.13/pandoc-2.13-windows-x86_64.zip" "$INSTDIR\pandoc.zip"
    ZipDLL::extractall "$INSTDIR\pandoc.zip" "$INSTDIR\src\main\resources\base"
    CopyFiles "$INSTDIR\wkhtmltox\bin\wkhtmltopdf.exe" "$INSTDIR\src\main\resources\base"
    WriteUninstaller "$INSTDIR\uninstaller.exe"
    Delete "$INSTDIR\pandoc.zip"
    Delete "$INSTDIR\wkhtmltox.7z"
    RMDir /r "$INSTDIR\wkhtmltox"
    CreateShortCut "$SMPROGRAMS\Pepys.lnk" "$INSTDIR\Pepys.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Pepys" "DisplayName" "Pepys"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Pepys" "UninstallString" "$\"$INSTDIR\uninstaller.exe$\""
SectionEnd

Section "Uninstall"
    RMDir /r "$INSTDIR"
    RMDir /r "$LocalAppdata\Pepys"
    Delete "$SMPROGRAMS\Pepys.lnk"
SectionEnd