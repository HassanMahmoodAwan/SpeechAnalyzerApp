from . import Prompts
import json

# ====== Using OpenAI Realtime API ======
def processing_RealtimeAPI(audio_fileName, client:any):
    
    with open(audio_fileName, "rb") as audio_file:
        data = audio_file.read()

    encoded_string = base64.b64encode(data).decode('utf-8')
    completion = client.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text"],
        messages=[
            {
                "role": "user",
                "content": [
                    { 
                        "type": "text",
                        "text": "I provided you a recording of Company Representive and Customer. Your job is to provide summary in roman Urdu, sentiments and Emotions of customer. Also provide problem statement of customer in roman urdu. provide satisfactor level of customer as well. Provide all mentioned things in Dictionary Format."
                    },
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": encoded_string,
                            "format": "mp3"
                        }
                    }
                ]
            },
        ]
    )
    return completion.choices[0].message




# ====== Using GPT-4o =======
def analysis_Sentiments_Emotions(transcript:str, client:any):
    # Lets work on Sentiment and Emotions
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": Prompts.analysis_Sentiment_Emotion},
            {"role": "user", "content": transcript}         
        ]
    )   
    data = json.loads(str(response.choices[0].message.content))

    sentiment = data.get("sentiment", {})
    emotion = data.get("emotion", {})

    return str(sentiment) + " " + str(emotion)
    


def processing_Summary_Topic(transcript:str, client:any):
    # Lets work on Sentiment and Emotions
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": Prompts.summary_topic},
            {"role": "user", "content": transcript}         
        ]
    )   
    
    data = json.loads(str(response.choices[0].message.content))

    sentiment = data.get("summary", {})
    emotion = data.get("topic", {})

    return str(sentiment) + " " + str(emotion)
