@echo off
REM Build exe file
pyinstaller --onefile --icon=app.ico --add-data "config.json:." dontkillmyvibe.py

echo.
echo ============================================
echo Build complete!
echo Exe location: dist\dontkillmyvibe.exe
echo Config file: Place config.json next to exe
echo ============================================
pause
