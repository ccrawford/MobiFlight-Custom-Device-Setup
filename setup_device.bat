@echo off
setlocal

:: Check if arguments are provided
if "%~1"=="" (
    echo Usage: setup_device.bat <device_name> <prefix>
    exit /b 1
)

if "%~2"=="" (
    echo Usage: setup_device.bat <device_name> <prefix>
    exit /b 1
)

:: Set variables
set DEVICE_NAME=%~1
set PREFIX=%~2

:: Clone the repository
echo Cloning CommunityTemplate repository...
git clone https://github.com/MobiFlight/CommunityTemplate.git %DEVICE_NAME%

if errorlevel 1 (
    echo Failed to clone repository. Exiting.
    exit /b 1
)

:: Run the Python script
echo Running MobiflightTemplater...
python ..\..\scripts\MobiflightTemplater.py .\%DEVICE_NAME% %DEVICE_NAME% %PREFIX%

if errorlevel 1 (
    echo Failed to run MobiflightTemplater script. Exiting.
    exit /b 1
)

:: Change directory to the new device folder
cd %DEVICE_NAME%

:: Remove the remote origin
echo Removing Git remote origin...
git remote remove origin

if errorlevel 1 (
    echo Failed to remove Git remote. Exiting.
    exit /b 1
)

:: Open in VS Code
echo Opening in VS Code...
code .

endlocal
