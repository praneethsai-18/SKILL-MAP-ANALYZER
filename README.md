# ⚡ SkillMap AI — Resume Skill Gap Analyzer

> Award-winning AI Career Intelligence Platform with ⚔️ Multi-Role Battle Mode

## 🚀 Quick Start (5 Steps)

```bash
# 1. Clone / extract project
cd skillmap-ai

# 2. Install server dependencies
cd server && npm install

# 3. Install client dependencies
cd ../client && npm install

# 4. Set up environment variables
cp ../server/.env.example ../server/.env
# Edit .env with your MongoDB URI

# 5. Run both servers
cd .. && npm run dev
```

App runs at: http://localhost:5173
API runs at: http://localhost:5000

## 📁 Project Structure

```
skillmap-ai/
├── client/          # React 18 + Vite frontend
├── server/          # Node.js + Express backend
├── data/            # Shared datasets (skills, roles, courses)
└── README.md
```

## 🛠️ Tech Stack

| Layer     | Technology                                 |
|-----------|--------------------------------------------|
| Frontend  | React 18, Vite, TailwindCSS, Framer Motion |
| Backend   | Node.js, Express.js                        |
| Database  | MongoDB + Mongoose                         |
| Charts    | Recharts                                   |
| Auth      | JWT + bcryptjs                             |
| Files     | pdf-parse, Mammoth                         |
| Reports   | PDFKit                                     |

## ✨ Features

- 📊 Single Role deep analysis
- ⚔️ Multi-Role Battle Mode (compare 3 roles simultaneously)
- 🧠 500+ skill taxonomy with weighted scoring
- 📚 Personalized 12-week learning roadmap
- 🤖 ATS compatibility simulation
- 📄 PDF report export
- 🎯 Interactive analytics dashboard
