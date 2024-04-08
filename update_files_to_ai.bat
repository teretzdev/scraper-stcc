@echo off
setlocal enabledelayedexpansion

rem Initialize the output file
set "outputFile=project_contents.txt"
if exist "%outputFile%" del "%outputFile%"

rem Step 1: Generate list of JavaScript files and their sizes
echo Generating list of JavaScript files and their sizes...
echo List of JavaScript files and their sizes: > "%outputFile%"
(for /f "delims=" %%i in ('dir /b /s *.js ^| findstr /v "\\node_modules\\"') do (
    set "size=%%~zi"
    echo File: %%i Size: !size! bytes >> "%outputFile%"
)) 

echo. >> "%outputFile%"
echo ===== Compiled JavaScript Files ===== >> "%outputFile%"
echo. >> "%outputFile%"

rem Step 2: Compile contents of JavaScript files
echo Compiling JavaScript files...
(for /f "delims=" %%i in ('dir /b /s *.js ^| findstr /v "\\node_modules\\"') do (
    echo ===== %%i ===== >> "%outputFile%"
    type "%%i" >> "%outputFile%"
    echo. >> "%outputFile%"
))

echo Compilation complete.

rem Step 3: Optional - Open the compiled file for review
start "%outputFile%"

endlocal
