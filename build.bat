@echo off
setlocal

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install pyinstaller if not already installed
pip install pyinstaller

REM Choose icon only if app.ico exists
set ICON_ARG=
if exist app.ico (
	set ICON_ARG=--icon=app.ico
) else (
	echo [warn] app.ico not found, building without custom icon
)

REM Clean previous build, build without console
pyinstaller --clean --noconfirm --onefile --noconsole %ICON_ARG% --add-data "config.json:." dontkillmyvibe.py

REM Copy config.json to dist folder
if not exist dist mkdir dist
copy /Y config.json dist\

echo.
echo ============================================
echo Build complete!
echo Exe location: dist\dontkillmyvibe.exe
echo Config file: dist\config.json (copied)
echo ============================================
pause
endlocal
