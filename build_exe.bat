@echo off
chcp 65001 >nul
echo.
echo ════════════════════════════════════════════════════════════════
echo    Building ToolAutoMail.exe with PyInstaller
echo ════════════════════════════════════════════════════════════════
echo.

REM Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] PyInstaller not found. Installing...
    python -m pip install pyinstaller
    echo.
)

echo [*] Building .exe file...
echo.

REM Clean old build
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build with PyInstaller
python -m PyInstaller --clean --onefile --name ToolAutoMail --console main.py

echo.
if exist dist\ToolAutoMail.exe (
    echo ════════════════════════════════════════════════════════════════
    echo    ✓ Build successful!
    echo ════════════════════════════════════════════════════════════════
    echo.
    echo    File location: dist\ToolAutoMail.exe
    echo.
    dir dist\ToolAutoMail.exe | find "ToolAutoMail.exe"
    echo.
    echo ════════════════════════════════════════════════════════════════
) else (
    echo ════════════════════════════════════════════════════════════════
    echo    ✗ Build failed!
    echo ════════════════════════════════════════════════════════════════
    exit /b 1
)

echo.
pause
