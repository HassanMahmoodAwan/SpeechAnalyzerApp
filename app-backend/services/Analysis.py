import re
import Prompts


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

    try:
        json.loads(output)
    except json.JSONDecodeError:
        return '{"error": "Invalid response format"}'

    return str(output)




#  ======== Sentiment Analysis OpenAI-o1 ==========
def sentimentAnalysis_o1(transcript:str, client:any):
    
    sentimentPrompt = f"""You are a sentiment analyzer model. Analyze the following text. Analyze it and provide me the sentiment which are: [ positive, negative, neutral ] with their percentage.  First with the highest percentage and then with the second highest percentage. Only provide the name and percentage of sentiment in a dictionary || JSON. No any other text. 
             Here are some Examples, 
             
             Transcript: ایک کسٹمر اپنے کریڈٹ کارڈ کے بارے میں معلومات حاصل کر رہا تھا۔ بینک نمائندے نے دو طرح کے کریڈٹ کارڈز، گولڈ اور پلیٹینم کے بارے میں بتایا، جن میں فیس اور کم از کم تنخواہ کے تقاضے شامل ہیں۔ گولڈ کارڈ کی فیس 2500 روپے اور پلیٹینم کارڈ کی فیس 5000 روپے ہوتی ہے۔ کسٹمر کو بتایا گیا کہ پلیٹینم کارڈ کے لیے زیادہ فوائد ہیں اور اس کی حد زیادہ ہوتی ہے۔ نمائندے نے درخواست کے عمل اور تنخواہ کی ضروریات کو بھی واضح کیا۔
             Sentiment: {{'neutral':80, 'positive':15, 'negative':5}}
             
             Transcript: The update caused a lot of bugs, and it's been frustrating. We lost a lot of time trying to fix the issues.
             Sentiment: {{'negative':85, 'neutral':15, 'positive':0}}
             
             Transcript: I love the new features you added to the app! It's so much more user-friendly now, and my team is very happy
             Sentiment: {{'positive':90, 'neutral':10, 'negative':0}}
             
             
             Ensure the result dictionary should not have any other word like json at the start of provided string, as I need to use it at frontend so format should be exact same.
             
             Provided Input Transcript is: {transcript}
             
             Thanks GPT"""
    
    
    
    
    response = client.chat.completions.create(
        model="o1-preview",
        messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": sentimentPrompt
                },
            ],
            
        }]    
        
    )
    return str(response.choices[0].message.content)



# ======== Emotion Analysis ============
def emotionAnalysis(transcript: str, sentiment, client: any):

    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"""You are an emotion analyzer model. Analyze the following text. Analyze it and provide me the emotion. Emotion should be three of the following: [ happy, sad, angry, fear, surprise, neutral, frustrated ]. The Sentiment of the following Input Transcript is {sentiment}. Only provide name and percentage of each emotion just in dictionary form. No other text or word. 
                
                Here are some Examples:

                Transcript: The update caused a lot of bugs, and it's been frustrating. We lost a lot of time trying to fix the issues.
                Emotion: {{'frustrated': 80, 'angry': 15, 'neutral': 5}}

                Transcript: ایک کسٹمر اپنے کریڈٹ کارڈ کے بارے میں معلومات حاصل کر رہا تھا۔ بینک نمائندے نے دو طرح کے کریڈٹ کارڈز، گولڈ اور پلیٹینم کے بارے میں بتایا، جن میں فیس اور کم از کم تنخواہ کے تقاضے شامل ہیں۔ گولڈ کارڈ کی فیس 2500 روپے اور پلیٹینم کارڈ کی فیس 5000 روپے ہوتی ہے۔ کسٹمر کو بتایا گیا کہ پلیٹینم کارڈ کے لیے زیادہ فوائد ہیں اور اس کی حد زیادہ ہوتی ہے۔ نمائندے نے درخواست کے عمل اور تنخواہ کی ضروریات کو بھی واضح کیا۔
                Emotion: {{'neutral': 70, 'happy': 20, 'surprise': 10}}

                Transcript: I love the new features you added to the app! It's so much more user-friendly now, and my team is very happy.
                Emotion: {{'joy': 85, 'happy': 15, 'neutral': 0}}

                Transcript: The project deadline was pushed back, but I don’t mind. It gives me more time to work on it.
                Emotion: {{'neutral': 60, 'happy': 25, 'joy': 15}}
                
                Ensure the result dictionary does not contain any additional words like "json", "emotion" at the start. The format must be exact as this is needed for frontend use. Thanks GPT
                """
            },
            {"role": "user", "content": transcript}
        ]
    )
    return response.choices[0].message.content




# ======== Emotion Analysis OpenAI-o1 ============
def emotionAnalysis_o1(transcript: str, client: any, sentiment: dict):
    
    emotionPrompt = f"""You are an emotion analyzer model. Analyze the following text. Analyze it and provide me the emotion. Emotion should be three of the following: [ happy, sad, angry, fear, surprise, neutral, frustrated ]. The Sentiment of the following Input Transcript is {sentiment}. Only provide name and percentage of each emotion just in dictionary form. No other text, just dictionary || Json. Ensure the resultant dictionary does not contain any additional words like "json" at the start
                
                Here are some Examples:

                Transcript: The update caused a lot of bugs, and it's been frustrating. We lost a lot of time trying to fix the issues.
                Emotion: {{'frustrated': 80, 'angry': 15, 'neutral': 5}}

                Transcript: ایک کسٹمر اپنے کریڈٹ کارڈ کے بارے میں معلومات حاصل کر رہا تھا۔ بینک نمائندے نے دو طرح کے کریڈٹ کارڈز، گولڈ اور پلیٹینم کے بارے میں بتایا، جن میں فیس اور کم از کم تنخواہ کے تقاضے شامل ہیں۔ گولڈ کارڈ کی فیس 2500 روپے اور پلیٹینم کارڈ کی فیس 5000 روپے ہوتی ہے۔ کسٹمر کو بتایا گیا کہ پلیٹینم کارڈ کے لیے زیادہ فوائد ہیں اور اس کی حد زیادہ ہوتی ہے۔ نمائندے نے درخواست کے عمل اور تنخواہ کی ضروریات کو بھی واضح کیا۔
                Emotion: {{'neutral': 70, 'happy': 20, 'surprise': 10}}

                Transcript: I love the new features you added to the app! It's so much more user-friendly now, and my team is very happy.
                Emotion: {{'joy': 85, 'happy': 15, 'neutral': 0}}

                Transcript: The project deadline was pushed back, but I don’t mind. It gives me more time to work on it.
                Emotion: {{'neutral': 60, 'happy': 25, 'joy': 15}}
                
                Ensure the result dictionary does not contain any additional words like "json" at the start. The format must be exact as this is needed for frontend use. 
                
                provided Input Transcript is : {transcript}
                
                Thanks GPT
                """
                
                
    messages = [{"role": "user", "content": emotionPrompt}]
    response = client.chat.completions.create(
        model="o1-preview",
        messages=messages
        
    )
    return response.choices[0].message.content



# Topic Extraction
def topicExtraction(transcript:str, client:any, summary):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You need to find the topic of the following text. Extract the topic from the following text. Go throught the Text and tell me about what is discussed in the text. Provide me the topic in 15-20 words or less. Language will be the same as the transcript provided to you, means if Urdu, then Topic will be in urdu, if english topic will be in English and simlar for other langauges."},
            {"role": "user", "content": transcript}
        ]
    )
    return str(response.choices[0].message.content)


# Topic Extraction OpenAI-o1

def topicExtraction_o1(transcript:str, client:any, summary):
    
    topicPrompt = f"""You need to find the topic of the following text. Extract the topic from the following text. Go throught the Text and tell me about what is discussed in the text. Provide me the topic in 15-20 words or less. Language will be the same as the transcript provided to you, means if Urdu, then Topic will be in urdu, if english topic will be in English and simlar for other langauges.
    
    Provided Input Transcript is {transcript}
    
    for reference Transcript summary is {summary}
    
    """
    
    messages = [{"role": "user", "content": topicPrompt}]
    response = client.chat.completions.create(
        model="o1-mini",
        messages=messages
    )
    return str(response.choices[0].message.content)



# Categorize the Text
def categorizeText(transcript:str, client:any):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a text categorizer. Categorize the following text. Categorize it and provide me the category. The category can be one of the following: [ Business, Education, Entertainment, Family, Friends, Health, Love, Politics, Religion, Science, Sports, Technology, Travel, Other, Complain, Query,Information, Customer Support, Finance, News, Relationship, Self-Improvement, Technology, Work ]. You can give me one to three categories. keep in mind no extra text. "},
            {"role": "user", "content": transcript}
        ]
    )
    return str(response.choices[0].message.content)



# Categorize the Text OpenAI-o1
def categorizeText_o1(transcript:str, client:any):
    
    catergoryPrompt = f"""You are a text categorizer. Categorize the following text. Categorize it and provide me the category. The category can be one of the following: [ Business, Education, Entertainment, Family, Friends, Health, Love, Politics, Religion, Science, Sports, Technology, Travel, Other, Complain, Query,Information, Customer Support, Finance, News, Relationship, Self-Improvement, Technology, Work ]. You can give me one to three categories. keep in mind no extra text. 
    
    Input Transcript is provided which is {transcript}
    """
    
    messages = [{"role": "user", "content": catergoryPrompt}]
    response = client.chat.completions.create(
        model="o1-mini",
        messages=messages
    )
    return str(response.choices[0].message.content)