from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import speechAnalyzerRoute
import models
from database import engine, SessionLocal

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(speechAnalyzerRoute.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Speech Analyzer API"}

