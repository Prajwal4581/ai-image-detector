# 🔍 AI Image Detector

Detects whether an uploaded image is **AI-generated or real** using:
- **Hive AI API** — detection model
- **LangChain + OpenAI** — explanation agent
- **FastAPI** — backend API
- **Streamlit** — frontend UI

---

## 🏗️ Architecture

```
User uploads image
      ↓
Streamlit Frontend (frontend/streamlit_app.py)
      ↓ HTTP POST /detect
FastAPI Backend (app/main.py)
      ↓
Hive AI API → detection score
      ↓
LangChain Agent → human-readable explanation
      ↓
JSON Response back to UI
```

---

## 🚀 Setup & Run

### 1. Clone and install dependencies
```bash
git clone <your-repo-url>
cd ai-detector
pip install -r requirements.txt
```

### 2. Set up API keys
```bash
cp .env.example .env
# Edit .env and add your API keys
```

Get your keys:
- OpenAI API key: https://platform.openai.com/api-keys
- Hive API key: https://thehive.ai (free tier available)

### 3. Run FastAPI backend
```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Run Streamlit frontend (new terminal)
```bash
streamlit run frontend/streamlit_app.py
```

### 5. Open browser
- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs  ← FastAPI auto-generates this!

---

## 🐳 Run with Docker
```bash
docker build -t ai-detector .
docker run -p 8000:8000 --env-file .env ai-detector
```

---

## 📁 Project Structure
```
ai-detector/
├── app/
│   ├── main.py          # FastAPI routes
│   ├── detector.py      # Hive AI API integration
│   └── agent.py         # LangChain explanation agent
├── frontend/
│   └── streamlit_app.py # Streamlit UI
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

---

## 🛠️ Tech Stack
| Layer | Technology |
|---|---|
| Backend API | FastAPI |
| AI Detection Model | Hive AI API |
| AI Agent / Explanation | LangChain + OpenAI GPT-3.5 |
| Frontend | Streamlit |
| Containerization | Docker |

---

## 🔮 Future Improvements
- [ ] Add video/deepfake detection support
- [ ] Batch image processing
- [ ] Detection history with database storage
- [ ] Confidence threshold configuration
- [ ] Support for more file formats
```
