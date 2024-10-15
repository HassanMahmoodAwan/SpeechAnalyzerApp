from services import *
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from openai import OpenAI
from dotenv import load_dotenv
import os
import zipfile
import shutil
from database import engine, SessionLocal
import models
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import Annotated, List, Optional
import time



load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

router = APIRouter()
client = OpenAI()

models.Base.metadata.create_all(bind=engine)

# Directory to store the audio files
DATASET_DIR = "Dataset/sourceFiles/"
UPLOAD_FOLDER = "./Dataset/uploaded_ZIP"
os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Global Variables
filename: str = ""
fileExtension: str = ""
fileDuration: str = ""
creationTime: str = ""


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]



# Upload audio file ROUTE
@router.post("/api/upload-and-analyze")
async def upload_audio(db: db_dependency, InputfileName = Form(...)):
        
    global filename, fileExtension, file_duration, creationTime
    filename = InputfileName
    fileExtension = InputfileName.split(".")[-1]


    print(" Analyzation Started")
    creationTime, fileDuration, processedAudio = preprocessing_audio(filename)
    print("Processed Audio")
    
    # transcript = transcribeAudio_whisperAPI(processedAudio, client)
    # print("Transcripted")
    
    # transcript = transcribeAudio_googleAPI(processedAudio)
    # print("Google-Transcripted")
    
    
    transcript = transcribeAudio_whisperLocal(processedAudio)
    print("Transcripted")
    
    
    translated_transcript = transcriptEnchancer(transcript, client)
    print("Roman Urdu Translator")
    
    diarized_Transcript = diarization_audio(translated_transcript, client)
    print("Dialog-flowTranscript")  
    
    summary = summarize_Transcript_o1(transcript, client)
    print("Summarized")
    
    sentiment = sentimentAnalysis_o1(translated_transcript, client)
    print("Sentiment")
    
    emotion = emotionAnalysis_o1(translated_transcript, client, sentiment)
    print("Emotion")
    
    topic = topicExtraction_o1(transcript, client, summary)
    print("Topic / Query")
    
    category = categorizeText_o1(transcript, client)
    print("Categorized")
    

    print("==== Storing Data in DB ====")
    db_analysis = models.Speech_Analysis_Table(
        filename = filename,
        file_extension = fileExtension,
        file_duration = fileDuration + " " + str(creationTime),
        transcript = transcript,
        summary = summary,
        translated_transcript = translated_transcript,
        diarized_transcript = diarized_Transcript,
        sentiment = sentiment,
        emotion = emotion,
        topic = topic,
        category = category
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    return {"status": "success", "message": "File uploaded and analyzed successfully", "filename": filename}



# Route to Fetch all Records from database
@router.get("/api/all-records")
async def get_all_data(db: db_dependency):
    db_table = models.Speech_Analysis_Table
    try:
        data = db.query(db_table).all()
        return data
    except Exception as e:
        return {"status": "Error Fetching Data (404)", "message": str(e)}


# Route to Fetch Record by ID
@router.get("/api/record-by-id/{id}")
async def get_record_by_id(id: str, db: db_dependency):
    id = int(id)
    db_table = models.Speech_Analysis_Table
    try:
        data = db.query(db_table).filter(db_table.id == id).first()
        if (data is None):
            return {"status": "Error", "message": "Data not found"}
        return data
    except Exception as e:
        return {"status": "error", "message": str(e)}




# Route to delete Record by ID from Database.
@router.delete("/api/delete-record-by-id/{id}")
async def delete_record_by_id(id: int, db: db_dependency):
    db_table = models.Speech_Analysis_Table
    try:
        data = db.query(db_table).filter(db_table.id == id).first()
        db.delete(data)
        db.commit()
        db.refresh(db)
        return {"status": "success", "message": "Data deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# ============= ZIP FOLDER UPLOAD ==============
@router.post("/api/upload-multiple-files")
async def upload_zip( file: UploadFile = File(...)):

    zip_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Unzip files & store in DATASET_DIR
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(DATASET_DIR)

    # Get all mp3 and wav files from unzipped folder
    extracted_files = [f for f in os.listdir(DATASET_DIR) if f.endswith(('.mp3', '.wav'))]
    
    return {"fileNamesList":extracted_files}

 
 
#  ========= File Upload (MP3 WAV FLAC) ==========
@router.post("/api/upload-audio")
async def upload_audio(file: UploadFile = File(...)):

    file_location = os.path.join(DATASET_DIR, file.filename)
    print("Hello")
    
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    return {"fileNamesList": [file.filename]}
