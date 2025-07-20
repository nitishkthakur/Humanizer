# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

**Run the application:**
```bash
python run.py
```
This starts the FastAPI server with hot reload on http://localhost:8000

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Environment setup:**
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

## Architecture Overview

This is a FastAPI web application for AI text humanization with two main features:

### Core Components

**Backend (`backend/main.py`):**
- FastAPI application with three main endpoints:
  - `GET /`: Serves the main interface
  - `POST /humanize`: Processes text humanization requests
  - `POST /chat`: Handles chat functionality
  - `POST /clear-chat`: Clears chat history
- Uses Groq API for LLM interactions
- In-memory chat session storage (keyed by session_id)
- Static file serving for frontend assets

**Text Humanization Engine (`humanize_using_groq.py`):**
- `HumanizeTextWithGroq` class handles the core humanization logic
- Processes text paragraph-by-paragraph for better results
- Supports multiple iteration passes (1-5) with different prompts per iteration
- Auto-detects paragraph boundaries and splits long content
- Uses different system prompts for each iteration to progressively improve humanization

**Frontend (`frontend/`):**
- Single-page application using Alpine.js for reactivity
- HTMX for seamless API interactions
- Two main pages: "Write & Humanize" and "Chat"
- Uses Marked.js for markdown rendering
- Professional dark blue theme with responsive design

### Key Features

**Text Humanization:**
- Multiple processing modes (currently only "llm_approach" is implemented)
- Model selection (defaults to llama-3.3-70b-versatile)
- Two-iteration humanization process with specialized prompts
- Real-time markdown rendering of results

**Chat Interface:**
- Persistent conversation history per session
- Model selection capability
- Markdown rendering of messages
- Chat clearing functionality

## Environment Requirements

- Python 3.7+
- GROQ_API_KEY environment variable (required)
- Internet connection for Groq API calls

## File Structure Notes

- `run.py`: Application entry point with development server configuration
- Frontend assets are served from `frontend/static/`
- Templates use Jinja2 and are located in `frontend/templates/`
- No test files or build scripts are present in this codebase
- No linting or formatting tools configured

## API Integration

All LLM interactions use the Groq API with configurable models. The humanization process specifically uses a multi-stage approach with different system prompts designed to progressively make text more natural and conversational.