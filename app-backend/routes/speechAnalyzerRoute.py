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



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]



# ===== ZIP FOLDER UPLOAD =====
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

 
 
#  ===== File Upload (MP3 WAV FLAC) =====
@router.post("/api/upload-audio")
async def upload_audio(file: UploadFile = File(...)):

    file_location = os.path.join(DATASET_DIR, file.filename)
    
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    return {"fileNamesList": [file.filename]}




# ===== Analyze audio file =====
@router.post("/api/upload-and-analyze")
async def upload_audio(db: db_dependency, InputfileName = Form(...)):
        
    filename = InputfileName
    fileExtension = InputfileName.split(".")[-1]

    print("Starting Analysis")
    creationTime, fileDuration, processedAudio = preprocessing_audio(filename)
    print("Processed Audio")
    
    # transcript = transcribeAudio_whisperAPI(processedAudio, client)
    # print("Audio Transcripted")
           
    transcript = transcribeAudio_whisperLocal(processedAudio)
    print("Audio Transcription (Done)")
     
    enhancedTranscript = transcriptEnchancer(transcript, client)
    # enhancedTranscript = transcript
    print("Transcription Enchanced (Done)")
    
    diarized_Transcript = diarization_audio(enhancedTranscript, client)
    # diarized_Transcript = ""
    print("Dialog-flow of Transcript (Done)")  
    
    summary = summarize_Transcript(enhancedTranscript, client)
    print("Summarized (Done)")
    
    # sentiment = analysis_Sentiments_Emotions(enhancedTranscript, client)
    sentiment = sentimentAnalysis(enhancedTranscript, client)
    print("Sentiment (Done)")
    
    # emotion = sentiment
    emotion = emotionAnalysis(enhancedTranscript, sentiment, client)
    print("Emotion (Done)")
    
    topic = topicExtraction(enhancedTranscript, client, summary)
    # topic = processing_Summary_Topic(transcript, client)
    print("Topic / Query (Done)")
    
    category = categorizeText(enhancedTranscript, client)
    print("Categorized (Done)")
    

    print("\nStoring results in Database \n")
    db_analysis = models.Speech_Analysis_Table(
        filename = filename,
        file_extension = fileExtension,
        file_duration = fileDuration + " " + str(creationTime),
        transcript = transcript,
        summary = summary,
        translated_transcript = enhancedTranscript,
        diarized_transcript = diarized_Transcript,
        sentiment = sentiment,
        emotion = emotion,
        topic = topic,
        category = category
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    return {"status": "success", "message": "File analyzed and Saved successfully", "filename": filename}



# ===== Fetch All Records ======
@router.get("/api/all-records")
async def get_all_records(db: db_dependency):
    db_table = models.Speech_Analysis_Table
    try:
        data = db.query(db_table).all()
        return data
    except Exception as e:
        return {"status": "Error Fetching Data (404)", "message": str(e)}


# ===== Fetch Record by ID ======
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
        return {"status": "Error", "message": str(e)}



# ===== Delete Record by ID ======
@router.delete("/api/delete-record-by-id/{id}")
async def delete_record_by_id(id: int, db: db_dependency):
    db_table = models.Speech_Analysis_Table
    try:
        data = db.query(db_table).filter(db_table.id == id).first()
        if not data:
            raise HTTPException(status_code=404, detail="Record not found")
        
        db.delete(data)
        db.commit()
        return {"status": "success", "message": "Data deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


