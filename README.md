# Resume Screener AI

An end-to-end machine learning web app that reads a resume (PDF or TXT) and predicts the best-fit job role, with a confidence score, top matches, detected skills, and a resume quality score.

**Live Demo:** [resume-screener-snowy.vercel.app](https://resume-screener-snowy.vercel.app/)
**Backend API:** [resume-screener-tf1e.onrender.com](https://resume-screener-tf1e.onrender.com)

> The backend runs on a free Render instance, so the first request after a period of inactivity may take a few seconds to respond.

---

## Features

- Upload a resume as **PDF or TXT**
- Predicts the **best-fit job role** with a confidence score
- Shows the **top 5 job matches** with progress bars
- **Auto-detects 40+ tech skills** from the resume
- Gives a **resume quality score**
- **Rejects non-resume files** before prediction

### Supported job categories

Full Stack Developer, Java Developer, Data Scientist, DevOps Engineer, Business Analyst, and Others.

---

## Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | React.js, Axios, Custom CSS |
| Backend | FastAPI, PyPDF2, Python 3.11 |
| Machine Learning | scikit-learn (Random Forest), TF-IDF Vectorizer, pandas, numpy, Pickle |
| Deployment | Vercel (frontend), Render (backend), UptimeRobot (uptime monitoring) |

---

## Machine Learning Pipeline

1. **Dataset:** 2,484 real resumes from Kaggle
2. **Cleaning:** text cleaned and prepared with pandas
3. **Feature extraction:** TF-IDF vectorization (3,000 features, bigrams)
4. **Split:** 80% training / 20% testing
5. **Model:** Random Forest classifier (200 trees)
6. **Result:** accuracy improved from **54% (KNN)** to **79% (Random Forest)**
7. **Serving:** model saved with Pickle and exposed as a REST API using FastAPI

---

## How It Works

1. The user uploads a resume in the React frontend.
2. The frontend sends the file to the FastAPI backend using Axios.
3. The backend extracts text (PyPDF2 for PDFs) and checks that the file looks like a resume.
4. The text is converted into TF-IDF features and passed to the Random Forest model.
5. The API returns the predicted role, confidence score, top 5 matches, detected skills, and quality score.
6. The frontend displays the results with progress bars.

---

## Run Locally

### Backend

```bash
git clone https://github.com/aaruhyareddy66/resume-screener.git
cd resume-screener

# create and activate a virtual environment (Python 3.11 recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm start
```

Set the backend URL in the frontend to `http://localhost:8000` when running locally.

> Adjust folder and file names above if your project structure differs.

---

## Challenges and Fixes

| Problem | Solution |
|---|---|
| numpy version mismatch between local (2.x) and Render (1.26.4) | Retrained the model on Render so the saved model matches the server environment |
| scikit-learn version mismatch with the `.pkl` files | Set `PYTHON_VERSION=3.11` on Render |
| Frontend was pushed as a Git submodule | Removed the inner `.git` folder |
| Vercel detected FastAPI instead of React | Deployed the frontend using the Vercel CLI |

---

## Future Improvements

- Add more job categories and a larger training dataset
- Try embedding-based models for better accuracy
- Show suggested skills to add for a target role

---

## Author

**Aaruhya Reddy**
GitHub: [@aaruhyareddy66](https://github.com/aaruhyareddy66)
