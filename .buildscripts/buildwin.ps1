Import-Module ps2exe
rm -Recurse ..\.win-build
mkdir ..\.win-build
cp -Recurse ..\src ..\.win-build
cp -Recurse ..\venv ..\.win-build
cp .\installer.nsi ..\.win-build
ps2exe .\runPepys.ps1 ..\.win-build\Pepys.exe -noConsole -noOutput -noError -iconFile ..\.win-build\src\main\resources\base\icons\appicons\pepys-icon.ico
