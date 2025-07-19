from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
from groq import Groq
import uvicorn

load_dotenv()

app = FastAPI(title="Humanizer", description="AI Text Humanization Tool")

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/humanize")
async def humanize_text(
    prompt: str = Form(...),
    mode: str = Form(...)
):
    try:
        if mode == "humanize":
            system_prompt = "You are an expert at humanizing AI-generated text. Take the provided text and rewrite it to sound more natural, conversational, and human-like while maintaining the original meaning. Remove any robotic or overly formal language patterns."
        else:  # using_llm mode
            system_prompt = "You are a helpful AI assistant. Respond to the user's request naturally and helpfully."
        
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=1000
        )
        
        result = completion.choices[0].message.content
        return {"success": True, "result": result}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/chat")
async def chat(message: str = Form(...)):
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Provide clear, concise, and helpful responses."},
                {"role": "user", "content": message}
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=1000
        )
        
        result = completion.choices[0].message.content
        return {"success": True, "result": result}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)