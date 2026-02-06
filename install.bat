@echo off
REM Occamy Field Operations System - Windows Installation Script

echo ================================================
echo Occamy Field Operations - Installation
echo ================================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)
echo [OK] Python found

REM Check pip
echo Checking pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not installed
    pause
    exit /b 1
)
echo [OK] pip found

REM Create virtual environment
echo.
echo Creating virtual environment...
if exist venv (
    echo [WARNING] Virtual environment already exists
    set /p RECREATE="Recreate it? (y/n): "
    if /i "%RECREATE%"=="y" (
        rmdir /s /q venv
        python -m venv venv
        echo [OK] Virtual environment recreated
    )
) else (
    python -m venv venv
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed

REM Setup environment file
echo.
echo Setting up environment...
if not exist .env (
    if exist .env.example (
        copy .env.example .env
        echo [OK] Created .env file
    )
)

REM Initialize database
echo.
echo Initializing database...
echo Please wait...
timeout /t 2 >nul
python app.py >nul 2>&1 &
timeout /t 5 >nul
taskkill /f /im python.exe >nul 2>&1

if exist occamy.db (
    echo [OK] Database initialized
    echo [INFO] Default admin: admin / admin123
) else (
    echo [ERROR] Database initialization failed
    pause
    exit /b 1
)

REM Ask about demo data
echo.
set /p DEMO="Load demo data? (y/n): "
if /i "%DEMO%"=="y" (
    python create_demo_data.py
    echo [OK] Demo data loaded
)

REM Completion
echo.
echo ================================================
echo Installation Complete!
echo ================================================
echo.
echo Next Steps:
echo   1. Start the application:
echo      python app.py
echo.
echo   2. Open in browser:
echo      http://localhost:5000
echo.
echo   3. Login:
echo      Username: admin
echo      Password: admin123
echo.
echo IMPORTANT: Change the default password immediately!
echo.
pause
