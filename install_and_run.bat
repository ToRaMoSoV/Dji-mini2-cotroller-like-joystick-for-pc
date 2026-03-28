@echo off
echo Installing required Python packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install packages. Make sure pip is installed and you have internet connection.
    pause
    exit /b 1
)
echo.
echo Starting the program...
python rc_to_xbox.py
pause
