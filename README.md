# Resume Screener AI

An ML-powered resume screening platform that analyzes your resume and predicts the best job role for you — built from scratch using real data, real ML, and real deployment.

**Live Demo:** https://resume-screener-snowy.vercel.app
Backend: https://resume-screener-tf1e.onrender.com

---

## What it does

Upload your resume and the ML model reads it, predicts your best job role, and shows top 5 matches with confidence scores. It also detects your skills automatically and gives a resume quality score.

---

## Features

- Upload PDF or TXT resume
- Random Forest model predicts best job role
- Shows top 5 job categories with confidence percentage
- Auto detects 40+ tech skills from resume
- Resume quality score based on content
- Rejects non-resume files like marksheets

---

## ML Pipeline
Real Dataset — 2484 resumes from Kaggle

Data cleaning with pandas

TF-IDF Vectorization — 3000 features with bigrams

Train / Test Split — 80% train, 20% test

Random Forest Classifier — 200 trees

79% Accuracy on test data

Model saved with Pickle

Deployed as REST API with FastAPI
---

## Model Performance

| Metric | Value |
|--------|-------|
| Accuracy | 79% |
| Training Samples | 2131 |
| Test Samples | 533 |
| Trees in Forest | 200 |
| TF-IDF Features | 3000 |
| Job Categories | 6 |

---

## Job Categories

- Full Stack Developer
- Java Developer
- Data Scientist
- DevOps Engineer
- Business Analyst
- Others

---

## Tech Stack

**Machine Learning** — scikit-learn, TF-IDF Vectorizer, pandas, numpy, Pickle

**Backend** — FastAPI, PyPDF2, Python 3.11, Uvicorn

**Frontend** — React.js, Axios, Custom CSS

**Deployment** — Vercel (frontend), Render (backend), GitHub, UptimeRobot

---

## Run Locally

```bash
# Backend
pip install -r requirements.txt
python train_model.py
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm start
```

---

## Project Structure
resume-screener/

├── main.py              — FastAPI backend

├── train_model.py       — ML model training script

├── model.pkl            — Trained Random Forest model

├── tfidf.pkl            — TF-IDF vectorizer

├── ResumeData.csv       — Kaggle dataset

├── requirements.txt     — Python dependencies

└── frontend/

└── src/

├── App.js       — Main React component

└── App.css      — Styling

## Author

Mallidi Venkata Aaruhya Reddy

GitHub: https://github.com/aaruhyareddy66
