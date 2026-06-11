# 📄 PDF Chat Assistant

An AI-powered PDF chat application using Flask, PyPDF, and Groq's LLM.

## Features

✅ Upload password-protected PDFs
✅ AI-powered Q&A from PDF content
✅ Conversation history tracking
✅ Beautiful UI with math formula rendering
✅ One-click Render deployment

## Local Setup

### Prerequisites
- Python 3.11+
- pip

### Installation

1. Clone the repository
```bash
git clone <repo-url>
cd password_bypass
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set environment variables
```bash
export GROQ_API_KEY=your_groq_api_key_here
# On Windows: set GROQ_API_KEY=your_groq_api_key_here
```

5. Run the application
```bash
python app.py
```

6. Open browser to `http://localhost:5000`

## Deployment on Render

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo>
git push -u origin main
```

### Step 2: Connect to Render
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select the repository and branch

### Step 3: Configure Deployment
- **Name**: pdf-assistant
- **Runtime**: Python 3.11
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

### Step 4: Set Environment Variables
In Render Dashboard → Environment:
- Add `GROQ_API_KEY` = your Groq API key

### Step 5: Deploy
Click "Deploy" and wait for the build to complete!

## How to Use

1. **Upload PDF**: Select a PDF file and enter password if encrypted
2. **Ask Questions**: Type any question about the PDF content
3. **View Answers**: AI-powered responses with beautiful formatting
4. **See History**: All conversation history is displayed
5. **Exit**: Type "exit" or click "Exit Chat" to start fresh

## Technologies Used

- **Backend**: Flask (Python web framework)
- **PDF Processing**: PyPDF
- **Embeddings**: Sentence Transformers
- **LLM**: Groq API (llama-3.3-70b-versatile)
- **Frontend**: HTML/CSS with KaTeX for math rendering

## Project Structure

```
password_bypass/
├── app.py                 # Flask application
├── pdf.py                # PDF processing & chat logic
├── templates/
│   └── index.html        # Web UI
├── uploads/              # Temporary PDF storage
├── requirements.txt      # Python dependencies
├── Procfile             # Render deployment config
└── render.yaml          # Render service config
```

## Getting Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Create API key
4. Copy and paste in environment variables

## Notes

- File uploads are temporary (deleted on app restart)
- Works best with PDFs under 50MB
- Each user's conversation is isolated per session
- Math formulas are rendered beautifully using KaTeX

## License

MIT License - Feel free to use this project!
