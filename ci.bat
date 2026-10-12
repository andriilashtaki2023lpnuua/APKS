@echo off
setlocal
cd /d "%~dp0"

set "BUILD_DIR=%~1"
if "%BUILD_DIR%"=="" set "BUILD_DIR=build"

cmake -S . -B "%BUILD_DIR%" -DCMAKE_BUILD_TYPE=Release
if errorlevel 1 exit /b 1

cmake --build "%BUILD_DIR%" --config Release
if errorlevel 1 exit /b 1

ctest --test-dir "%BUILD_DIR%" -C Release --output-on-failure
if errorlevel 1 exit /b 1