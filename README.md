# Humanizer

A professional AI text processing tool with two main functionalities: text humanization and AI chat. Built with FastAPI backend and modern frontend technologies.

## Features

- **Write & Humanize**: Transform AI-generated text into natural, human-like content
- **Chat**: Interactive conversation with AI
- Professional dark blue theme with responsive design
- Modern UI with Alpine.js and HTMX
- Powered by Groq LLM

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

3. **Run the Application**
   ```bash
   python run.py
   ```

4. **Access the App**
   Open your browser and go to: `http://localhost:8000`

## Project Structure

```
Humanizer/
├── backend/
│   └── main.py              # FastAPI application
├── frontend/
│   ├── templates/
│   │   └── index.html       # Main HTML template
│   └── static/
│       ├── css/
│       │   └── styles.css   # Professional styling
│       └── js/
│           └── app.js       # Alpine.js functionality
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── run.py                  # Application launcher
```

## API Endpoints

- `GET /`: Main application interface
- `POST /humanize`: Process text for humanization or LLM response
- `POST /chat`: Chat functionality

## Technologies Used

- **Backend**: FastAPI, Groq API
- **Frontend**: HTML5, CSS3, Alpine.js, HTMX
- **Styling**: Custom CSS with professional dark blue theme
- **AI**: Groq LLM (llama3-8b-8192)

## Usage

### Write & Humanize Page
1. Enter your text or prompt in the input area
2. Select processing mode:
   - **HumanizeAI**: Transforms text to sound more natural and human-like
   - **Using LLM**: Processes the prompt with AI assistance
3. Click "Humanize" to process
4. View results in the output sections

### Chat Page
- Type your message and press Enter or click Send
- Have a natural conversation with the AI assistant
- Message history is maintained during the session

## Requirements

- Python 3.7+
- Groq API key
- Internet connection for API calls
