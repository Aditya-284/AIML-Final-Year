#!/usr/bin/env python3
"""
Main entry point for the Synthetic Data Generator API
"""

import uvicorn
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    # Configuration: bind to localhost by default so the URL is clickable
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print(f"Starting Synthetic Data Generator API on {host}:{port}")
    print(f"Reload mode: {reload}")
    print(f"Virtual environment: {sys.prefix}")
    # Helpful clickable URL
    print(f"Open http://localhost:{port}  (Swagger UI: http://localhost:{port}/docs)")
    
    # Run the server
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
