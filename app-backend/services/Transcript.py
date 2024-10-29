import re           
import json
import os
import numpy as np
import torch
import whisper
from . import Prompts

# ====== Google API Imports ========
from google.cloud.speech_v2 import SpeechClient
from google.api_core import client_options
from google.cloud.speech_v2.types import cloud_speech
from google.cloud import speech
from google.cloud import storage 
from google.auth import default
# ==================================



# # Global Variables
DEVICE = "cuda" if torch.cuda.is_available()  else "mps" if torch.backends.mps.is_available()  else "cpu"
MODEL = whisper.load_model("base", DEVICE)


#  ======== Whisper OpenAI API ==========
def transcribeAudio_whisperAPI(audio_filePath:str, client:any) -> str:
    with open(audio_filePath, "rb") as audio_file:
        try:
            transcript= client.audio.transcriptions.create(model="whisper-1", file=audio_file)
        except Exception as e:
            raise Exception(f"Error while Performing Transcript:  {e}")
    
    return  transcript.text



# ======== Whisper Local Large =========
def transcribeAudio_whisperLocal(audio_filePath:str) -> str:
    
    # result = model.transcribe(audio_filePath,
    #                       prompt= Prompts.transcript_WhisperLocal,
    #                       temperature=0.2,       
    #                       beam_size=8,
    #                       ) 
    # transcript = result["text"] 
    # return transcript 
       
    return " اسلام علیکم ملار فرمنکن سے میں نیمل بات کر رہی ہوں فاہمے کیا مدد کر سکتے ہو؟ نیمل وقار بات کر رہا ہوں کیسے ہوں؟ اللہم دلاللہ میں صحبہ وقار ٹھیک ہوں امید ہے آپ بھی خیریت سے ہوں گے جی اللہ کا شکر اچھا ہوں مجھے کچھ انفومیشن چاہیے کہ پہلے سے میں ٹیپن انٹر کر کے آیا ہوں ٹھیک ہے تو آپ کے پاس ریکارڈ آ رہا ہے ویسے ٹیپن ٹیپن میں دوبارہ ویفائی کروارہتے ہیں ویسے سینئیسین گنسٹاپ کا ریٹا آ رہا ہے ویفائی کر دیں گے نہیں میں انٹر کر کے آیا ہوں مجھے یہ پوچھنا ہے کہ ایبیل کریڈیٹ کارڈ کے بارے میں کہ ایبیل کریڈیٹ کارڈ پروائیڈ کرتا ہے کریڈیٹ کارڈ کی سرویس بلکل لائٹ بنک کے دو کریڈیٹ کارڈ ہیں میں آپ کو ان دونوں کے حوالے سے سر وقار گائیڈ کر دیتی ہوں مجھے جس اتنا کنفرم کی جائے گا اس کے ڈیفرنٹ کرائیڈیٹیرئیس ہوتے ہیں ایک سیلوری پرسن کے لیے ہوتا ہے اور ایک بزنس پرسن کے لیے ہوتا ہے آپ کو کون سے کرائیڈیٹ کارڈ ہے سیلوری پرسن کے لیے پوچھنا چاہ رہے ہیں میں آپ کو کنفرم کر دیتی ہوں اگر آپ سیلوری پرسن کے لیے پوچھنا چاہ رہے ہیں تو اس کا جو الیجیبیٹی کرائیڈیٹیرئیس سبقار یہ ہے کہ آپ کا لائسٹ سکس منٹ کے ساتھ علائٹمنٹ کے ساتھ ریلیشیشپ ہونا چاہیے منیمم سکس منٹ کا اور منیمم ہر مہنٹ آپ کے اکاؤنٹ میں سیلوری 25,000 کی آنی چاہیے اور جو سکس منٹ ہوں گے ان سکس منٹ میں ہر مہینے آپ کے اکاؤنٹ میں ایک رقم لائسٹ نہیں آنی چاہیے یہ اس کا کرائیڈیریا ہے اس کے علاوہ کارڈ دو طرح کی ہیں رقم کتنی مطلب 25,000 کے رقم ہر مہینے اکاؤنٹ میں آنی چاہیے منیمم نہیں منیمم آنی چاہیے اور جو سیونگ ہونی چاہیے وہ بھی تو بول رہے ہیں نا ایسا کچھ نہیں لکھا ہوا جو بیسک کرائیڈیریا ہے بیسک کرائیڈیریا کو یہاں سے گائیٹ کیا جارہا ہے بیسک الیجیویٹی کرائیڈیریا یہ ہے اس کے علاوہ دو طرح کے کارڈ ہیں کریڈیٹ کارڈ ایک گولڈ ہے اور ایک پلاتینم کارڈ ہے اگر گولڈ کارڈ ہی بات کریں تو اس کی انویل سی ہے 2500 پلس ایف ایٹی 2500 جرم ایٹ اینویل سی ہے اور گولڈ میں جو اکو لیمٹ ملتی ہے وہ ملتی ہے 30,000 سے لے کے 5 لاکھ ترکی اس کے علاوہ دوسرا کارڈ ہے پلاتینم کے اس کی انویل سی ہے 5000 جرم ایٹ اینویل سی اور اس میں اکو لیمٹ ملتی ہے 3 لاکھ سے 2 ملین ترکی یہ لیمٹس ہیں اور گولڈ کارڈ کا ریورسل کرائیٹیریا یہ ہے اگر 2500 سے سپینڈنگ کر لیتے ہیں 90 دنوں میں تو فی ریورس ہو جاتی ہے پلاتینم کارڈ میں اگر 5000 کے سپینڈنگ ہوتی ہیں 90 دن میں تو اس کی بھی فی ریورس ہو جاتی ہے ٹھیک ہے اور دوسرا مجھے یہ بتائیے اگر میں نے اس کو اپلائے کرنا ہو تو کیا کرائیٹیریا ہے اگر اپلائے کرنا ہو تو ہم یہاں سے آپ کے نیشل ریکویسٹ لیتے ہیں انیشل ریکویسٹ آپ پین جگہوں سے بنوا سکتے ہیں برانچ کے ذریعے دے سکتے ہیں ہیلپ لنگ کے ذریعے دے سکتے ہیں اور اگر ورڈس ایپ سرویس اسمال کرتے ہیں تو ورڈس ایپ کے ذریعے بھی آپ انیشل ریکویسٹ فارورٹ کروا سکتے ہیں یہاں سے سب انیشل ریکویسٹ فارورٹ ہوتی ہے جو کہ کریٹکار ڈپارٹمنٹ کے پاس جاتی ہے اگر تو آپ الیجیبل ہوں تو وہ پھر آپ کو خود کسٹمہ کو کانٹیکٹ کر کے پردر انفرمیشن جو بھی ہے وہ لے لیتے ہیں ہم سے میں لاہور سے تعلق رکھتا ہوں میری سلری جو ہوتی ہے دپوزٹ وہ بھی ایویل کے اکانٹ کے اندر ہوتی ہے تو مجھے پردر تو اسی چیز کے ضرورت نہیں ہوگی کسی ڈاکننٹ میں آرہا ہے اگر ہوئی بھی تو وہ تو ویسے بھی آپ کو ڈپارٹمنٹ خود کانٹیکٹ کر لیتا ہے کیونکہ ہم تو یہاں سے اگر ریکویسٹ آپ دیتے بھی ہیں تو صرف انیشئل ریکویسٹ آگے فارورڈ ہوتی ہیں ہماری انٹرے باقی جو بھی فالور پہلا جو بھی پروسیجر ہے وہ تکریل کارٹ ڈپارٹن والے اپنا خود کرتے ہیں چلے ٹھیک ہے میں تینکیو فور انفرمیشن اگر مجھے ریکویسٹ ڈال لیں تو میں انشاءاللہ دوبارہ کال کر کے انیشئل ریکویسٹ چکریہ کچھ اور جانا چاہیں گے چکریہ کال فیڈلے کے جانے چانسر کروں گے لائف آو بینکن کال کریں گے شکریہ لائف آو بینکن" 
    




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