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
import re
from datetime import datetime
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

def sanitize_unicode_text(text: str) -> str:
    """
    Clean text to remove invalid Unicode surrogate characters that cause encoding errors.
    
    Args:
        text: Input text that may contain problematic Unicode characters
        
    Returns:
        Cleaned text safe for UTF-8 encoding
    """
    if not text:
        return text
    
    # Remove or replace Unicode surrogate characters (U+D800 to U+DFFF)
    # These are invalid in UTF-8 and cause encoding errors
    sanitized = text.encode('utf-8', 'replace').decode('utf-8')
    
    # Remove any remaining problematic characters
    # This regex removes characters that might cause issues
    sanitized = re.sub(r'[\uD800-\uDFFF]', '', sanitized)
    
    # Also remove any null bytes or other control characters that might cause issues
    sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', sanitized)
    
    return sanitized

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/humanize")
async def humanize_text(
    prompt: str = Form(...),
    mode: str = Form(...),
    model: str = Form(default="llama-3.3-70b-versatile"),
    iterations: int = Form(default=2),
    ai_response: str = Form(default="")
):
    try:
        if mode == "llm_approach":
            # Use the HumanizeTextWithGroq class with the selected model
            text_to_humanize = ai_response if ai_response.strip() else prompt
            
            if not text_to_humanize.strip():
                return {"success": False, "error": "No text available to humanize. Please generate content first."}
            
            # Sanitize input text to prevent Unicode encoding errors
            text_to_humanize = sanitize_unicode_text(text_to_humanize)
            
            # Log humanization request start
            timestamp = datetime.now().strftime("%H:%M:%S")
            word_count = len(text_to_humanize.split())
            print(f"\n[{timestamp}] 📨 HUMANIZATION REQUEST RECEIVED")
            print(f"[{timestamp}] 🎯 Model: {model}")
            print(f"[{timestamp}] 🔄 Iterations: {iterations}")
            print(f"[{timestamp}] 📝 Input text: {word_count} words")
            print(f"[{timestamp}] 🔧 Mode: {mode}")
            
            # Initialize the humanizer with the selected model
            humanizer = HumanizeTextWithGroq(api_key=groq_api_key, model=model)
            
            # Validate iterations range (1-5)
            iterations = max(1, min(iterations, 5))
            
            # Humanize the text with user-specified iterations
            result = humanizer.humanize_text(text_to_humanize, n_iterations=iterations)
            
            # Sanitize output text to prevent Unicode encoding errors
            result = sanitize_unicode_text(result)
            
            # Log completion
            result_word_count = len(result.split())
            final_timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{final_timestamp}] ✅ HUMANIZATION REQUEST COMPLETED")
            print(f"[{final_timestamp}] 📤 Output: {result_word_count} words")
            print(f"[{final_timestamp}] 📊 Word count change: {result_word_count - word_count:+d} words")
            
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
        
        # Sanitize user message and add to conversation history
        message = sanitize_unicode_text(message)
        chat_sessions[session_id].append({"role": "user", "content": message})
        
        # Log chat request details
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n[{timestamp}] 💬 CHAT REQUEST TO GROQ")
        print(f"[{timestamp}] 🎯 Model: {model}")
        print(f"[{timestamp}] 🆔 Session ID: {session_id}")
        print(f"[{timestamp}] 📝 User Message: {message}")
        print(f"[{timestamp}] 📚 Conversation History Length: {len(chat_sessions[session_id])} messages")
        
        # Prepare and log the full payload
        groq_payload = {
            "messages": chat_sessions[session_id],
            "model": model,
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        print(f"[{timestamp}] 📦 FULL GROQ PAYLOAD:")
        print(f"[{timestamp}]   Model: {groq_payload['model']}")
        print(f"[{timestamp}]   Temperature: {groq_payload['temperature']}")
        print(f"[{timestamp}]   Max Tokens: {groq_payload['max_tokens']}")
        print(f"[{timestamp}]   Messages ({len(groq_payload['messages'])}):")
        for i, msg in enumerate(groq_payload['messages']):
            content_preview = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
            print(f"[{timestamp}]     {i+1}. {msg['role']}: {content_preview}")
        print(f"[{timestamp}] " + "="*50)
        
        # Get completion with full conversation history
        completion = client.chat.completions.create(**groq_payload)
        
        result = completion.choices[0].message.content
        
        # Sanitize the AI response
        result = sanitize_unicode_text(result)
        
        # Log response details
        response_timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n[{response_timestamp}] ✅ GROQ RESPONSE RECEIVED")
        print(f"[{response_timestamp}] 📤 Response Length: {len(result)} characters")
        print(f"[{response_timestamp}] 📝 Response Preview: {result[:150]}{'...' if len(result) > 150 else ''}")
        print(f"[{response_timestamp}] 🔄 Updated conversation history to {len(chat_sessions[session_id]) + 1} messages")
        
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