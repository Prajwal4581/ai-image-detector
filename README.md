# 🔍 AI Image Detector

An AI-powered web app that detects whether an uploaded image is **AI-generated or real**, with intelligent explanation of the verdict.

## 🌐 Live Demo
> Run locally following setup instructions below

---

## 🏗️ Architecture

```
User uploads image
      ↓
Streamlit Frontend (frontend/streamlit_app.py)
      ↓ HTTP POST /detect
FastAPI Backend (app/main.py)
      ↓
Sightengine API → AI detection score
      ↓
Groq LLaMA3 → human-readable explanation
      ↓
JSON Response → displayed on UI
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI + Uvicorn |
| AI Detection Model | Sightengine API |
| AI Explanation Agent | Groq API (LLaMA3-8b) |
| Frontend UI | Streamlit |
| Containerization | Docker |

---

## ✨ Features

- Upload JPG, PNG, or WEBP images
- Instant AI vs Real verdict with confidence score
- AI-powered explanation of WHY the image was flagged
- Clean progress bar showing AI generation probability
- Error handling and file size validation
- REST API with auto-generated Swagger docs

---

## 🚀 Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/Prajwal4581/ai-image-detector.git
cd ai-image-detector
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API keys
```bash
cp .env.example .env
# Edit .env and add your keys
```

Get your free API keys:
- Groq API key → https://console.groq.com
- Sightengine keys → https://sightengine.com

Your `.env` should look like:
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxx
SIGHTENGINE_USER=your_user_id
SIGHTENGINE_SECRET=your_secret
```

### 5. Run FastAPI backend
```bash
uvicorn app.main:app --reload --port 8000
```

### 6. Run Streamlit frontend (new terminal)
```bash
venv\Scripts\activate
streamlit run frontend/streamlit_app.py
```

### 7. Open browser
- Frontend → http://localhost:8501
- API Docs → http://localhost:8000/docs

---

## 🐳 Docker
```bash
docker build -t ai-image-detector .
docker run -p 8000:8000 --env-file .env ai-image-detector
```

---

## 📁 Project Structure
```
ai-image-detector/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI routes + validation
│   ├── detector.py      # Sightengine API integration
│   └── agent.py         # Groq LLaMA3 explanation agent
├── frontend/
│   └── streamlit_app.py # Streamlit UI
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

---

## 📸 Sample Results

| Image Type | Verdict | Confidence |
|---|---|---|
| Real photo | ✅ Real / Authentic | 99% |
| AI generated (Midjourney/DALL-E) | 🤖 AI Generated | 99% |

---

## 🔮 Future Improvements
- [ ] Video / deepfake detection
- [ ] Batch image processing
- [ ] Detection history with database
- [ ] Deploy on Render with live URL
- [ ] Add more detection models for ensemble voting
