import re
from . import Prompts


# Sentiment Analysis
def sentimentAnalysis(transcript:str, client:any):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": Prompts.analysis_Sentiments},
            {"role": "user", "content": transcript}         
        ]
    )   
    output = response.choices[0].message.content.strip()
    output = re.sub(r"^Sentiment:\s*", "", output)
    output = output.strip("```\njson```").strip()

    return str(output)



# Emotion Analysis
def emotionAnalysis(transcript: str, sentiment, client: any):
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": Prompts.analysis_Emotions(sentiment)
            },
            {"role": "user", "content": transcript}
        ]
    )   
    output = response.choices[0].message.content.strip()
    output = re.sub(r"^Emotion:\s*", "", output)

    return str(output)



# Topic Extraction
def topicExtraction(transcript:str, client:any, summary):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": Prompts.analysis_Topic},
            {"role": "user", "content": transcript}
        ]
    )
    return str(response.choices[0].message.content)



# Categorize the Text
def categorizeText(transcript:str, client:any):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": Prompts.analysis_Category},
            {"role": "user", "content": transcript}
        ]
    )
    return str(response.choices[0].message.content)