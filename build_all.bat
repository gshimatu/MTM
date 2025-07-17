@echo off
REM Nettoyage des anciens builds
echo Nettoyage des anciens builds...
rmdir /s /q dist
rmdir /s /q build
del /q *.spec

REM Compilation de app.py
echo Compilation de app.py...
pyinstaller --onefile --add-data "static;static" --add-data "templates;templates" --add-data "bin;bin" app.py

REM Compilation de launcher.py
echo Compilation de launcher.py...
pyinstaller --onefile --icon=logo.ico --name=Mtm launcher.py

REM Création du dossier final
echo Préparation du dossier final...
mkdir final
copy dist\app.exe final\
copy dist\Mtm.exe final\

REM (Optionnel) Copier les dossiers si besoin
REM xcopy static final\static /E /I
REM xcopy templates final\templates /E /I
REM xcopy bin final\bin /E /I

echo.
echo Build terminé !
echo Les exécutables sont dans le dossier 'final'
pause
