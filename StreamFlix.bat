@echo off
:: Setează variabila de director curent pentru a fi directorul în care se află acest script
set "CURRENT_DIR=%~dp0"

:: Schimbă directorul curent la directorul în care se află scriptul
cd /d "%CURRENT_DIR%"

:: Deschide un nou terminal și rulează comanda Python
start cmd /k "python app.py"
