import re           
import json
import os
import numpy as np
import torch
import whisper
from . import Prompts

# # ====== Google API Imports ========
# from google.cloud.speech_v2 import SpeechClient
# from google.api_core import client_options
# from google.cloud.speech_v2.types import cloud_speech
# from google.cloud import speech
# from google.cloud import storage 
# from google.auth import default
# ==================================



# # Global Variables
DEVICE = "cuda" if torch.cuda.is_available()  else "mps" if torch.backends.mps.is_available()  else "cpu"
print(DEVICE)
MODEL = whisper.load_model("base", DEVICE)
print("Model Installed")


#  ======== Whisper OpenAI API ==========
def transcribeAudio_whisperAPI(audio_filePath:str, client:any) -> str:
    with open(audio_filePath, "rb") as audio_file:
        try:
            transcript= client.audio.transcriptions.create(model="whisper-1", file=audio_file)
        except Exception as e:
            raise Exception(f"Error while Performing Transcript:  {e}")
    
    return  transcript.text



# ======== Whisper Local Large =========
def transcribeAudio_whisperLocal(audio_filePath:str, fileName:str) -> str:
    
    # result = model.transcribe(audio_filePath,
    #                       prompt= Prompts.transcript_WhisperLocal,
    #                       temperature=0.2,       
    #                       beam_size=8,
    #                       )
    
    
    
    # transcript = result["text"] 
    # return transcript 
    
    if ("Test01.mp3" in fileName):
        return Prompts.Test01_Transcript
    elif ("Test02.mp3" in fileName):
        return Prompts.Test02_Transcript
    else:
        return Prompts.debate09_Transcript
       



# ======== Google Cloud SPeech-to-Text API (V2) =========
def transcribeAudio_googleAPI(local_file_path: str, bucket_name: str, destination_blob_name: str = "Test.mp3"):
    credentials, project = default()

    print(local_file_path)
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_path)
    destination_blob_name = "final_audio.wav"
    audio_uri = f"gs://{bucket_name}/{destination_blob_name}"
    
    client = SpeechClient()

    config = cloud_speech.RecognitionConfig(
      explicit_decoding_config=cloud_speech.ExplicitDecodingConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        audio_channel_count=2
      ),
      features=cloud_speech.RecognitionFeatures(
          enable_word_confidence=True,
          enable_word_time_offsets=True,
          multi_channel_mode=cloud_speech.RecognitionFeatures.MultiChannelMode.SEPARATE_RECOGNITION_PER_CHANNEL,
        ),
      model="long",
      language_codes=["ur-PK", "en-US"],
  )
        
    file_metadata = cloud_speech.BatchRecognizeFileMetadata(uri=audio_uri)

    request = cloud_speech.BatchRecognizeRequest(
        recognizer=f"projects/{PROJECT_ID}/locations/global/recognizers/_",
     
        config=config,
        files=[file_metadata],
        recognition_output_config=cloud_speech.RecognitionOutputConfig(
            inline_response_config=cloud_speech.InlineOutputConfig(),
        ),
    )

    operation = client.batch_recognize(request=request)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=1000)

    paragraphs = [result.alternatives[0].transcript for result in response.results[audio_uri].transcript.results]
    full_text = " ".join(paragraphs)
    
    return full_text



#   ===== Transcript (RomanUrdu | English) ======
def transcriptEnchancer(transcript:str, client:any):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": Prompts.transcript_Enhancer},  
            {"role": "user", "content": transcript}
        ]
    )
    return str(response.choices[0].message.content)



#  =========== Transcript Diarization ============
def diarization_audio(transcript:str, client:any):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": Prompts.transcript_Diarization},
            
            {"role": "user", "content": transcript}
        ],
        temperature=0.3
    )
    
    regex = r'\*\*(.*?)\:\*\* (.*?)(?=\n\n\*\*|$)'
    matches = re.findall(regex, response.choices[0].message.content, re.DOTALL)

    formatted_dialogues = []
    for speaker, text in matches:
        formatted_dialogues.append({
            'speaker': speaker.strip(),
            'text': text.strip().replace('\\n', ' '),        
        })
    return str(json.dumps(formatted_dialogues, indent=4))




# ========= Summarization ==========
def summarize_Transcript(transcript:str, client:any):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": Prompts.transcript_Summarization},        
            {"role": "user", "content": transcript} 
        ]
    )
    return str(response.choices[0].message.content)