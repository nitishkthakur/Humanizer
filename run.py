import sys
import os
import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.main import app
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Humanizer application...")
    print("📝 Make sure to set your GROQ_API_KEY in a .env file")
    print("🌐 Application will be available at: http://localhost:8000")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)