@echo off
title The Remy Digest - Newsroom Console
color 0f

echo ========================================================
echo        THE REMY DIGEST - AUTOMATED NEWSROOM
echo ========================================================
echo.

:: Step 0: Gather Intel (New Step)
echo [1/4] Scouring the wires for news (NT News / Local)...
python gather_headlines.py
echo.

:: Step 1: Write the Stories
echo [2/4] Interrogating AI Reporters...
python generate_news.py
if %ERRORLEVEL% NEQ 0 (
    echo Error generating news. Halting.
    pause
    exit /b
)
echo.

:: Step 2: Develop the Photos
echo [3/4] Opening Darkroom...
python generate_images.py
if %ERRORLEVEL% NEQ 0 (
    echo Error generating images. Halting.
    pause
    exit /b
)
echo.

:: Step 3: Print the Paper
echo [4/4] Printing the edition...
python build.py
if %ERRORLEVEL% NEQ 0 (
    echo Error building site. Halting.
    pause
    exit /b
)

echo.
echo ========================================================
echo        SUCCESS! ISSUE PUBLISHED TO /OUTPUT
echo ========================================================
echo.
pause