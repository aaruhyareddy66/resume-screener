from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
import pickle
import PyPDF2
import io
import re

app = FastAPI()

@app.middleware("http")
async def cors_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        response = JSONResponse(content={}, status_code=200)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and vectorizer
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('tfidf.pkl', 'rb') as f:
    tfidf = pickle.load(f)

# Resume keywords to validate file is actually a resume
RESUME_KEYWORDS = [
    'experience', 'education', 'skills', 'work', 'project',
    'university', 'college', 'degree', 'internship', 'career',
    'objective', 'summary', 'certification', 'achievement', 'employment'
]

def extract_text_from_pdf(file_bytes):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def clean_text(text):
    text = re.sub(r'http\S+', ' ', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.lower().strip()

def is_resume(text):
    text_lower = text.lower()
    matches = sum(1 for keyword in RESUME_KEYWORDS if keyword in text_lower)
    return matches >= 3

def clean_preview(text):
    # Remove placeholder text
    text = re.sub(r'\[.*?\]', '', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()[:500]

@app.get("/")
def home():
    return {"message": "resume screener api is running"}

@app.post("/predict")
async def predict_resume(file: UploadFile = File(...)):
    # Check file type
    if not file.filename.endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF or TXT files are accepted!")

    file_bytes = await file.read()

    # Extract text
    if file.filename.endswith('.pdf'):
        text = extract_text_from_pdf(file_bytes)
    else:
        text = file_bytes.decode('utf-8', errors='ignore')

    # Validate it's actually a resume
    if not is_resume(text):
        raise HTTPException(
            status_code=400,
            detail="This doesn't look like a resume. Please upload a valid resume!"
        )

    # Check minimum content
    if len(text.strip()) < 100:
        raise HTTPException(status_code=400, detail="Resume content is too short!")

    cleaned = clean_text(text)
    vectorized = tfidf.transform([cleaned])

    prediction = model.predict(vectorized)[0]
    probabilities = model.predict_proba(vectorized)[0]
    classes = model.classes_

    top_5 = sorted(zip(classes, probabilities), key=lambda x: x[1], reverse=True)[:5]

    return {
        "predicted_category": prediction,
        "confidence": round(float(max(probabilities)) * 100, 2),
        "top_5_matches": [
            {"category": cat, "score": round(float(prob) * 100, 2)}
            for cat, prob in top_5
        ],
        "text_preview": clean_preview(text),
        "full_text": clean_text(text)[:2000]
    }