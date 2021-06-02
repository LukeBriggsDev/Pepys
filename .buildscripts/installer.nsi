Outfile "pepys_install.exe"
Caption "Pepys"
InstallDir "$PROGRAMFILES64\Pepys"
Section "Install"
    SetOutPath "$INSTDIR"
    File /r enchant
    File /r PyQt5
    File /r regex
    File /r resources
    File /r yaml
    File *
    WriteUninstaller "$INSTDIR\uninstaller.exe"
    CreateShortCut "$SMPROGRAMS\Pepys.lnk" "$INSTDIR\Pepys.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Pepys" "DisplayName" "Pepys"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Pepys" "UninstallString" "$\"$INSTDIR\uninstaller.exe$\""
SectionEnd

Section "Uninstall"
    RMDir /r "$INSTDIR"
    RMDir /r "$LocalAppdata\Pepys"
    Delete "$SMPROGRAMS\Pepys.lnk"
SectionEnd