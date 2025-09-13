#!/usr/bin/env python3
"""
Synthetic Data Generator Launcher
Automatically starts the API server and opens the website
"""

import subprocess
import webbrowser
import time
import requests
import os
import sys
from pathlib import Path

def check_server_running():
    """Check if the server is already running"""
    try:
        response = requests.get("http://localhost:8000/docs", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_server():
    """Start the API server"""
    print("🚀 Starting API Server...")
    
    # Get the current directory
    current_dir = Path(__file__).parent
    venv_python = current_dir / ".venv" / "Scripts" / "python.exe"
    server_script = current_dir / "run_server.py"
    
    if not venv_python.exists():
        print("❌ Virtual environment not found!")
        print("Please run: python -m venv .venv")
        return None
    
    if not server_script.exists():
        print("❌ run_server.py not found!")
        return None
    
    # Start the server process
    try:
        process = subprocess.Popen(
            [str(venv_python), str(server_script)],
            cwd=str(current_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return process
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

def wait_for_server(max_wait=60):
    """Wait for the server to be ready"""
    print("⏳ Waiting for server to start...")
    
    for i in range(max_wait):
        if check_server_running():
            print("✅ Server is ready!")
            return True
        time.sleep(1)
        if i % 5 == 0 and i > 0:
            print(f"   Still waiting... ({i}s)")
    
    print("❌ Server failed to start within 60 seconds")
    return False

def open_website():
    """Open the website in the default browser"""
    current_dir = Path(__file__).parent
    html_file = current_dir / "synthetic_data_frontend.html"
    
    if html_file.exists():
        print("🌐 Opening website...")
        webbrowser.open(f"file://{html_file.absolute()}")
        return True
    else:
        print("❌ Website file not found!")
        return False

def main():
    """Main launcher function"""
    print("=" * 50)
    print("🎯 Synthetic Data Generator Launcher")
    print("=" * 50)
    
    # Check if server is already running
    if check_server_running():
        print("✅ Server is already running!")
        open_website()
        return
    
    # Start the server
    process = start_server()
    if not process:
        return
    
    # Wait for server to be ready
    if not wait_for_server():
        process.terminate()
        return
    
    # Open the website
    if open_website():
        print("\n🎉 Application started successfully!")
        print("📊 API Server: http://localhost:8000")
        print("🌐 Website: Opened in browser")
        print("\nPress Ctrl+C to stop the server")
        
        try:
            # Keep the launcher running
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            process.terminate()
            process.wait()
            print("✅ Server stopped")
    else:
        process.terminate()

if __name__ == "__main__":
    main()
