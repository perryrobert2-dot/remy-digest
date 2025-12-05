@echo off
title The Remy Digest - Newsroom Console
color 0f

echo ========================================================
echo        THE REMY DIGEST - AUTOMATED NEWSROOM
echo ========================================================
echo.

:: Step 0: Gather Intel
echo [1/5] Scouring the wires for news...
python gather_headlines.py
echo.

:: Step 1: Write the Stories
echo [2/5] Interrogating AI Reporters...
python generate_news.py
if %ERRORLEVEL% NEQ 0 (
    echo Error generating news. Halting.
    pause
    exit /b
)
echo.

:: Step 2: Develop the Photos
echo [3/5] Opening Darkroom...
python generate_images.py
if %ERRORLEVEL% NEQ 0 (
    echo Error generating images. Halting.
    pause
    exit /b
)
echo.

:: Step 3: Print the Paper
echo [4/5] Printing the edition...
python build.py
if %ERRORLEVEL% NEQ 0 (
    echo Error building site. Halting.
    pause
    exit /b
)
echo.

:: Step 4: Distribution
echo [5/5] Delivering to the World (Pushing to GitHub)...
git add .
git commit -m "New Issue Published: %date% %time%"
git push origin main

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo -------------------------------------------------------
    echo ERROR: The delivery truck broke down.
    echo Likely cause: You need to sign in.
    echo Try running 'git push' manually to see the error.
    echo -------------------------------------------------------
    pause
    exit /b
)

echo.
echo ========================================================
echo        SUCCESS! ISSUE IS LIVE ON THEREMYVERSE.COM
echo ========================================================
echo.
pause