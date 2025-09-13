@echo off
echo Starting Synthetic Data Generator...
echo.

REM Start the API server in the background
start "API Server" cmd /k ".venv\Scripts\python.exe run_server.py"

REM Wait a moment for server to start
timeout /t 3 /nobreak > nul

REM Open the website
start "" "synthetic_data_frontend.html"

echo.
echo ✅ Application started!
echo - API Server: Running in new window
echo - Website: Opening in browser
echo.
echo Press any key to close this window...
pause > nul
