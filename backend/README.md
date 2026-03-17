# SkillMap AI — Pure ML Backend
## No external APIs. spaCy + BERT + MongoDB. Everything runs locally.

---

## How It Works

```
Resume PDF/Text
      ↓
  pdfplumber (text extraction)
      ↓
  spaCy NLP (entity + noun phrase matching)
  +
  BERT Embeddings (semantic similarity)
  +
  Exact Keyword Matching
      ↓
  Skill Gap Analyzer (weighted scoring)
      ↓
  MongoDB (save results)
      ↓
  JSON Response → Frontend
```

---

## Folder Structure

```
skillmap-ml/
├── main.py                     ← FastAPI app — all endpoints
├── requirements.txt            ← Python packages
├── .env.example                ← Copy to .env
│
├── data/
│   └── skill_taxonomy.py       ← 500+ skills + role profiles
│
├── extractors/
│   ├── resume_parser.py        ← PDF/DOCX/text parser
│   └── skill_extractor.py      ← spaCy + BERT skill extraction
│
├── analyzers/
│   ├── skill_analyzer.py       ← Match scoring engine
│   └── battle_analyzer.py      ← Multi-role battle mode
│
├── database/
│   └── connection.py           ← MongoDB connection + collections
│
└── scripts/
    └── setup.py                ← Download ML models (run once)
```

---

## Setup — Step by Step

### Step 1 — Install Python packages

```powershell
cd skillmap-ml
pip install -r requirements.txt
```

### Step 2 — Download ML models (run once)

```powershell
python scripts/setup.py
```

This downloads:
- spaCy English model (~12MB)
- BERT all-MiniLM-L6-v2 (~80MB)
- NLTK data

### Step 3 — Install MongoDB (free)

Download Community Edition:
https://www.mongodb.com/try/download/community

Install with default settings.
MongoDB runs on localhost:27017 automatically.

OR skip MongoDB — the app works without it
(results just won't be saved to database)

### Step 4 — Configure .env

```powershell
copy .env.example .env
```

Edit `.env`:
```
MONGODB_URI=mongodb://localhost:27017
DB_NAME=skillmap_ai
```

### Step 5 — Start the backend

```powershell
python -m uvicorn main:app --reload --port 8000
```

### Step 6 — Open frontend

In a second terminal:
```powershell
cd ..\frontend
python -m http.server 3000
```

Open browser: http://localhost:3000

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health` | DB connection status |
| POST | `/analyze` | Upload PDF + roles → analysis |
| POST | `/analyze-text` | Paste text + roles → analysis |
| GET | `/roles` | List all 13+ available roles |
| GET | `/skills/trending` | Most common skills seen |
| GET | `/analyses/history` | Recent analyses from DB |
| GET | `/stats` | Usage statistics |

---

## ML Models Used

| Model | Purpose | Size |
|-------|---------|------|
| spaCy en_core_web_sm | Entity recognition, noun phrases | 12MB |
| BERT all-MiniLM-L6-v2 | Semantic skill similarity | 80MB |
| Custom skill matcher | Exact + alias keyword matching | 0MB |

---

## MongoDB Collections

| Collection | Purpose |
|------------|---------|
| analyses | Stores every analysis result |
| resumes | Caches parsed resume data |
| skills | Tracks skill frequency |

---

## Troubleshooting

**"No module named spacy"**
```powershell
pip install spacy
python -m spacy download en_core_web_sm
```

**"No module named sentence_transformers"**
```powershell
pip install sentence-transformers
```

**"MongoDB connection failed"**
- Install MongoDB Community: https://www.mongodb.com/try/download/community
- Or the app runs fine without it (no result saving)

**"No skills found in resume"**
- Make sure the resume contains actual skill names
- Try pasting the text directly instead of uploading PDF

**CORS error from frontend**
- Make sure you're opening frontend via `http://localhost:3000`
- NOT by double-clicking the HTML file
