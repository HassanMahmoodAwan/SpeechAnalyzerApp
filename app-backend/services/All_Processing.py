from . import Prompts
import json
import re
import base64

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
                        "text": """ I have provided a recording of a Company Representative and a Customer. Your task is to generate a structured output in Roman Urdu with the following elements:

                        1- Summary: A concise, 5-7 sentence summary of the conversation in Roman Urdu.
                        2- Problem Statement: A 1-2 sentence description highlighting the customer's main issue.
                        3- Sentiment: A single-word sentiment (e.g., Positive, Negative, Neutral) with describing the overall mood of the customer, with context.
                        4- Emotion: A single-word emotion (e.g., Frustration, Satisfaction, Curiosity), with context from the conversation.
                        5- Satisfaction Level: A rating of the customer's satisfaction level (e.g., High, Medium, Low).
                        
                        Output Format: Please return the output in a consistent JSON format as shown below:
                        
                        {
                            "summary": "5-7 sentence summary in Roman Urdu",
                            "problem_statement": "1-2 sentence problem statement in Roman Urdu",
                            "sentiment": "Single-word sentiment with 'highlighted context'",
                            "emotion": "Single-word emotion with 'highlighted context'",
                            "satisfaction_level": "High/Medium/Low"
                        }
                        
                        Please ensure that the summary, problem statement, and satisfaction level adhere to the specified lengths, and maintain a structured, clear format in JSON form.                      
                        """
                    },
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": encoded_string,
                            "format": "wav"
                        }
                    }
                ]
            },
        ]
    )
    return completion.choices[0].message.content




# ====== Using GPT-4o =======
def analysis_Sentiments_Emotions(transcript:str, client:any):
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": Prompts.analysis_Sentiment_Emotion},
            {"role": "user", "content": transcript}         
        ]
    )  
    print(str(response.choices[0].message.content).strip("```json\n```").strip()) 
    data = json.loads(str(response.choices[0].message.content).strip("```json\n```").strip())

    sentiment = data.get("sentiment", {})
    emotion = data.get("emotion", {})

    return str(sentiment), str(emotion)
    


def processing_Summary_Topic(transcript:str, client:any):
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": Prompts.summary_topic},
            {"role": "user", "content": transcript}         
        ]
    )   
    output = re.sub(r"^output:\s*", "", str(response.choices[0].message.content).strip("```\njson```").strip())
    print(output)
    data = json.loads(output)

    summary = data.get("summary", {})
    topic = data.get("topic", {})
    
    return str(summary), str(topic)
