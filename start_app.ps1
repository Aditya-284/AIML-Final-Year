Write-Host "Starting Synthetic Data Generator..." -ForegroundColor Green
Write-Host ""

# Start the API server in background
$job = Start-Job -ScriptBlock {
    Set-Location "D:\Specialization Project"
    .\.venv\Scripts\python.exe run_server.py
}

Write-Host "API Server starting..." -ForegroundColor Yellow

# Wait for server to be ready
$maxAttempts = 30
$attempt = 0
do {
    Start-Sleep -Seconds 2
    $attempt++
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/docs" -TimeoutSec 2 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ API Server is ready!" -ForegroundColor Green
            break
        }
    }
    catch {
        Write-Host "Waiting for server... ($attempt/$maxAttempts)" -ForegroundColor Yellow
    }
} while ($attempt -lt $maxAttempts)

if ($attempt -eq $maxAttempts) {
    Write-Host "❌ Server failed to start" -ForegroundColor Red
    exit 1
}

# Open the website
Start-Process "synthetic_data_frontend.html"

Write-Host ""
Write-Host "✅ Application started successfully!" -ForegroundColor Green
Write-Host "- API Server: Running in background" -ForegroundColor Cyan
Write-Host "- Website: Opening in browser" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow

# Keep the script running
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
}
finally {
    Write-Host "Stopping server..." -ForegroundColor Yellow
    Stop-Job $job
    Remove-Job $job
}
