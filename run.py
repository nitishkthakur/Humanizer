import uvicorn

if __name__ == "__main__":
    print("Starting Humanizer application...")
    print("Make sure to set your GROQ_API_KEY in a .env file")
    print("Application will be available at: http://localhost:8000")
    print("=" * 50)
    
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)