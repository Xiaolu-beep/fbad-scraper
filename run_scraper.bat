@echo off
title Van Scraper

echo Starting Ollama server...
start /min ollama serve

timeout /t 5 /nobreak >nul

echo Running scraper...
python van_monitor.py

echo.
echo Scraper finished. Closing Ollama...
taskkill /f /im ollama.exe >nul 2>&1
taskkill /f /im ollama_runner.exe >nul 2>&1

echo Done.
pause