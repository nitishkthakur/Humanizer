from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
from groq import Groq
import uvicorn
from typing import List, Dict
import sys
sys.path.append('..')
from humanize_using_groq import HumanizeTextWithGroq

load_dotenv()

app = FastAPI(title="Humanizer", description="AI Text Humanization Tool")

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# Initialize Groq client with proper error handling
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable is required")

client = Groq(api_key=groq_api_key)

# In-memory storage for chat conversations (in production, use a database)
chat_sessions: Dict[str, List[Dict[str, str]]] = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/humanize")
async def humanize_text(
    prompt: str = Form(...),
    mode: str = Form(...),
    model: str = Form(default="llama-3.3-70b-versatile"),
    ai_response: str = Form(default="")
):
    try:
        if mode == "llm_approach":
            # Use the HumanizeTextWithGroq class with the selected model
            text_to_humanize = ai_response if ai_response.strip() else prompt
            
            if not text_to_humanize.strip():
                return {"success": False, "error": "No text available to humanize. Please generate content first."}
            
            # Initialize the humanizer with the selected model
            humanizer = HumanizeTextWithGroq(api_key=groq_api_key, model=model)
            
            # Humanize the text with 2 iterations as requested
            result = humanizer.humanize_text(text_to_humanize, n_iterations=2)
            
            return {"success": True, "result": result}
        
        else:
            # For any other mode (including work_in_progress), return an error
            return {"success": False, "error": "This mode is not implemented yet."}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/chat")
async def chat(
    message: str = Form(...),
    model: str = Form(default="llama-3.3-70b-versatile"),
    session_id: str = Form(default="default")
):
    try:
        # Initialize session if it doesn't exist
        if session_id not in chat_sessions:
            chat_sessions[session_id] = [
                {"role": "system", "content": "You are a helpful AI assistant. Provide clear, concise, and helpful responses."}
            ]
        
        # Add user message to conversation history
        chat_sessions[session_id].append({"role": "user", "content": message})
        
        # Get completion with full conversation history
        completion = client.chat.completions.create(
            messages=chat_sessions[session_id],
            model=model,
            temperature=0.7,
            max_tokens=4000
        )
        
        result = completion.choices[0].message.content
        
        # Add assistant response to conversation history
        chat_sessions[session_id].append({"role": "assistant", "content": result})
        
        return {"success": True, "result": result}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/clear-chat")
async def clear_chat(session_id: str = Form(default="default")):
    try:
        # Clear the conversation history for the session
        if session_id in chat_sessions:
            chat_sessions[session_id] = [
                {"role": "system", "content": "You are a helpful AI assistant. Provide clear, concise, and helpful responses."}
            ]
        
        return {"success": True, "message": "Chat history cleared"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)