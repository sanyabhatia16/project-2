from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langauge_services import analyze_text

app = FastAPI(title="TextInsight AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "TextInsight AI Backend Running"}


@app.post("/analyze")
def analyze(request: TextRequest):
    return analyze_text(request.text)