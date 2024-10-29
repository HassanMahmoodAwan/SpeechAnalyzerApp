import re           
import json
import os
import numpy as np
import torch
import whisper

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

# PROJECT_ID = "zeta-stacker-437604-e0"
# BUCKET_NAME = "speechanalyzerbucket" 


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
    #                       prompt="""Transcribe the following conversation between a customer and a company representative. The conversation might be in Urdu or English, you have to figure out. There will be some words related to banking or any complain, such as 'اے بی ایل', 'الائیڈ بینک', 'کریڈٹ کارڈ', 'بینک', 'برانچ', 'پن', 'savings', 'لمیٹ', 'ensure', 'پالیسی', 'واٹس ایپ', 'انفارمیشن', 'کریڈینشلز', 'منتھ', 'پلاٹینم', 'گولڈ', 'سکس', 'مینجر, 'Policy' and other banking-related words. Donot convert english words into urdu, Show them as it is. Please ensure accurate transcription of both Urdu and English words in context.""",
    #                       temperature=0.2,       
    #                       beam_size=8,
    #                       ) 
    # transcript = result["text"]  
       
    transcript = " اسلام علیکم ملار فرمنکن سے میں نیمل بات کر رہی ہوں فاہمے کیا مدد کر سکتے ہو؟ نیمل وقار بات کر رہا ہوں کیسے ہوں؟ اللہم دلاللہ میں صحبہ وقار ٹھیک ہوں امید ہے آپ بھی خیریت سے ہوں گے جی اللہ کا شکر اچھا ہوں مجھے کچھ انفومیشن چاہیے کہ پہلے سے میں ٹیپن انٹر کر کے آیا ہوں ٹھیک ہے تو آپ کے پاس ریکارڈ آ رہا ہے ویسے ٹیپن ٹیپن میں دوبارہ ویفائی کروارہتے ہیں ویسے سینئیسین گنسٹاپ کا ریٹا آ رہا ہے ویفائی کر دیں گے نہیں میں انٹر کر کے آیا ہوں مجھے یہ پوچھنا ہے کہ ایبیل کریڈیٹ کارڈ کے بارے میں کہ ایبیل کریڈیٹ کارڈ پروائیڈ کرتا ہے کریڈیٹ کارڈ کی سرویس بلکل لائٹ بنک کے دو کریڈیٹ کارڈ ہیں میں آپ کو ان دونوں کے حوالے سے سر وقار گائیڈ کر دیتی ہوں مجھے جس اتنا کنفرم کی جائے گا اس کے ڈیفرنٹ کرائیڈیٹیرئیس ہوتے ہیں ایک سیلوری پرسن کے لیے ہوتا ہے اور ایک بزنس پرسن کے لیے ہوتا ہے آپ کو کون سے کرائیڈیٹ کارڈ ہے سیلوری پرسن کے لیے پوچھنا چاہ رہے ہیں میں آپ کو کنفرم کر دیتی ہوں اگر آپ سیلوری پرسن کے لیے پوچھنا چاہ رہے ہیں تو اس کا جو الیجیبیٹی کرائیڈیٹیرئیس سبقار یہ ہے کہ آپ کا لائسٹ سکس منٹ کے ساتھ علائٹمنٹ کے ساتھ ریلیشیشپ ہونا چاہیے منیمم سکس منٹ کا اور منیمم ہر مہنٹ آپ کے اکاؤنٹ میں سیلوری 25,000 کی آنی چاہیے اور جو سکس منٹ ہوں گے ان سکس منٹ میں ہر مہینے آپ کے اکاؤنٹ میں ایک رقم لائسٹ نہیں آنی چاہیے یہ اس کا کرائیڈیریا ہے اس کے علاوہ کارڈ دو طرح کی ہیں رقم کتنی مطلب 25,000 کے رقم ہر مہینے اکاؤنٹ میں آنی چاہیے منیمم نہیں منیمم آنی چاہیے اور جو سیونگ ہونی چاہیے وہ بھی تو بول رہے ہیں نا ایسا کچھ نہیں لکھا ہوا جو بیسک کرائیڈیریا ہے بیسک کرائیڈیریا کو یہاں سے گائیٹ کیا جارہا ہے بیسک الیجیویٹی کرائیڈیریا یہ ہے اس کے علاوہ دو طرح کے کارڈ ہیں کریڈیٹ کارڈ ایک گولڈ ہے اور ایک پلاتینم کارڈ ہے اگر گولڈ کارڈ ہی بات کریں تو اس کی انویل سی ہے 2500 پلس ایف ایٹی 2500 جرم ایٹ اینویل سی ہے اور گولڈ میں جو اکو لیمٹ ملتی ہے وہ ملتی ہے 30,000 سے لے کے 5 لاکھ ترکی اس کے علاوہ دوسرا کارڈ ہے پلاتینم کے اس کی انویل سی ہے 5000 جرم ایٹ اینویل سی اور اس میں اکو لیمٹ ملتی ہے 3 لاکھ سے 2 ملین ترکی یہ لیمٹس ہیں اور گولڈ کارڈ کا ریورسل کرائیٹیریا یہ ہے اگر 2500 سے سپینڈنگ کر لیتے ہیں 90 دنوں میں تو فی ریورس ہو جاتی ہے پلاتینم کارڈ میں اگر 5000 کے سپینڈنگ ہوتی ہیں 90 دن میں تو اس کی بھی فی ریورس ہو جاتی ہے ٹھیک ہے اور دوسرا مجھے یہ بتائیے اگر میں نے اس کو اپلائے کرنا ہو تو کیا کرائیٹیریا ہے اگر اپلائے کرنا ہو تو ہم یہاں سے آپ کے نیشل ریکویسٹ لیتے ہیں انیشل ریکویسٹ آپ پین جگہوں سے بنوا سکتے ہیں برانچ کے ذریعے دے سکتے ہیں ہیلپ لنگ کے ذریعے دے سکتے ہیں اور اگر ورڈس ایپ سرویس اسمال کرتے ہیں تو ورڈس ایپ کے ذریعے بھی آپ انیشل ریکویسٹ فارورٹ کروا سکتے ہیں یہاں سے سب انیشل ریکویسٹ فارورٹ ہوتی ہے جو کہ کریٹکار ڈپارٹمنٹ کے پاس جاتی ہے اگر تو آپ الیجیبل ہوں تو وہ پھر آپ کو خود کسٹمہ کو کانٹیکٹ کر کے پردر انفرمیشن جو بھی ہے وہ لے لیتے ہیں ہم سے میں لاہور سے تعلق رکھتا ہوں میری سلری جو ہوتی ہے دپوزٹ وہ بھی ایویل کے اکانٹ کے اندر ہوتی ہے تو مجھے پردر تو اسی چیز کے ضرورت نہیں ہوگی کسی ڈاکننٹ میں آرہا ہے اگر ہوئی بھی تو وہ تو ویسے بھی آپ کو ڈپارٹمنٹ خود کانٹیکٹ کر لیتا ہے کیونکہ ہم تو یہاں سے اگر ریکویسٹ آپ دیتے بھی ہیں تو صرف انیشئل ریکویسٹ آگے فارورڈ ہوتی ہیں ہماری انٹرے باقی جو بھی فالور پہلا جو بھی پروسیجر ہے وہ تکریل کارٹ ڈپارٹن والے اپنا خود کرتے ہیں چلے ٹھیک ہے میں تینکیو فور انفرمیشن اگر مجھے ریکویسٹ ڈال لیں تو میں انشاءاللہ دوبارہ کال کر کے انیشئل ریکویسٹ چکریہ کچھ اور جانا چاہیں گے چکریہ کال فیڈلے کے جانے چانسر کروں گے لائف آو بینکن کال کریں گے شکریہ لائف آو بینکن" 
    return transcript




# Google Cloud SPeech-to-Text API (V2)
def transcribeAudio_googleAPI(local_file_path: str, bucket_name: str = BUCKET_NAME, destination_blob_name: str = "Test.mp3"):
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
    print(full_text)
    
    return full_text



#   ===== Roman Urdu Transcript ======
def transcriptEnchancer(orignal_transcript:str, client:any):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": (
         """"If the input transcript is in English, enhance it by correcting grammar and logical flow while maintaining the original meaning. Provide the improved English transcript as the output.

        If the input is in Urdu, act as an expert Roman Urdu translator and translate the transcript into Roman Urdu (Urdu written with English alphabets). Ensure the translation is grammatically correct, has proper sentence structure, and only contains Romanized text.
        
        Ensure that common English words remain intact and some words need to be corrected, you can use them from provided list (Assalam o Alaikum, baat, T-PIN, six months, PIN, Allied Bank, CreditCard, DebitCard, Information, Platinium, Gold, ABL, Branch, PIN, Tax, Month, Six, Whatsapp, Enter,Tax, FED, Plus, Online Portal, Account, Manager, Name, Sir, City, Lahore, etc). In transcript, repetion of words should be avoided and remove extra words which seems noisey, but length of transcript should remain same as input I provided to you. Note that Bank Name is Allied Bank Limited, it needs to be always correct."""
    )},
            
            {"role": "user", "content": orignal_transcript}
        ]
    )
    return str(response.choices[0].message.content)



#  ==== Transcript Diarization ====
def diarization_audio(transcript:str, client:any):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """Your task is to diarize the transcript of a call between a company representative and a customer. Do not assign specific names; instead, use the tags 'company representative' and 'customer'. The call may involve a customer complaint, query, or a call initiated by the company to provide assistance or information.

            Ensure that you accurately segment the transcript into these two roles based on the conversation's context. The call could be initiated by either party, so determine the respective speaker for each part of the transcript accordingly. Accuracy is crucial, so maintain a high level of contextual understanding while assigning parts of the transcript to the appropriate speaker."""},
            
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





# ==== Summarization using OpenAI-O1 MODEL =====
def summarize_Transcript_o1(transcript:str, client:any):
    
    summaryPrompt = f"""You are a transcript summarizer. Summarize the following transcript in the same language as the input, and correct any spelling mistakes. Provide a concise and accurate summary in a single paragraph, without including the word 'summary' in the text. Also donot mention name of persons, instead use customer or company representative as this transcript is between customer and company.

    For example, your output should look like this:

    'While addressing a customer complaint, the company representative asked the customer for the order number and verified the information. The customer reported that their device was not turning on even when connected to a power outlet. The representative suggested removing and reconnecting the battery and trying a different outlet. The customer responded angrily, but the representative continued explaining that no extra cable was included because the item was discounted. The representative informed the customer that a new cable could be purchased and obtained within 24 hours, but the customer declined. The conversation ended with the customer expressing dissatisfaction with the vendor.'

    Note: The summary must be in the language of the transcript, i.e., if the transcript is in Urdu, the summary should be in Urdu; if it's in English, provide the summary in English, and so on. The output should follow the exact format as shown above, as it will be displayed on the frontend.
             
             Provided input Transcript is: {transcript}
             
             """
    messages = [{"role": "user", "content": summaryPrompt}]
    response = client.chat.completions.create(
        model="o1-mini",
        messages= messages
    )
    return str(response.choices[0].message.content)





# ==== Summarization =====
def summarize_Transcript(transcript:str, client:any):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """You are a transcript summarizer. Summarize the following transcript in the same language as the input, and correct any spelling mistakes. Provide a concise and accurate summary in a single paragraph, without including the word 'summary' in the text.

        For example, your output should look like this:

        'While addressing a customer complaint, the company representative asked the customer for the order number and verified the information. The customer reported that their device was not turning on even when connected to a power outlet. The representative suggested removing and reconnecting the battery and trying a different outlet. The customer responded angrily, but the representative continued explaining that no extra cable was included because the item was discounted. The representative informed the customer that a new cable could be purchased and obtained within 24 hours, but the customer declined. The conversation ended with the customer expressing dissatisfaction with the vendor.'

        Note: The summary must be in the language of the transcript, i.e., if the transcript is in Urdu, the summary should be in Urdu; if it's in English, provide the summary in English, and so on. The output should follow the exact format as shown above, as it will be displayed on the frontend."""},
            
            {"role": "user", "content": transcript} 
        ]
    )
    return str(response.choices[0].message.content)