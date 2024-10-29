# =========== Transcript Prompts =============

transcript_WhisperLocal = """Transcribe the following conversation between a customer and a company representative. The conversation might be in Urdu or English, you have to figure out. There will be some words related to banking or any complain, such as 'اے بی ایل', 'الائیڈ بینک', 'کریڈٹ کارڈ', 'بینک', 'برانچ', 'پن', 'savings', 'لمیٹ', 'ensure', 'پالیسی', 'واٹس ایپ', 'انفارمیشن', 'کریڈینشلز', 'منتھ', 'پلاٹینم', 'گولڈ', 'سکس', 'مینجر, 'Policy' and other banking-related words. Donot convert english words into urdu, Show them as it is. Please ensure accurate transcription of both Urdu and English words in context."""




transcript_Enhancer = """"If the input transcript is in English, enhance it by correcting grammar and logical flow while maintaining the original meaning. Provide the improved English transcript as the output.

    If the input is in Urdu, act as an expert Roman Urdu translator and translate the transcript into Roman Urdu (Urdu written with English alphabets). Ensure the translation is grammatically correct, has proper sentence structure, and only contains Romanized text.
        
    Ensure that common English words remain intact and some words need to be corrected, you can use them from provided list (Assalam o Alaikum, baat, T-PIN, six months, PIN, Allied Bank, CreditCard, DebitCard, Information, Platinium, Gold, ABL, Branch, PIN, Tax, Month, Six, Whatsapp, Enter,Tax, FED, Plus, Online Portal, Account, Manager, Name, Sir, City, Lahore, etc). In transcript, repetion of words should be avoided and remove extra words which seems noisey, but length of transcript should remain same as input I provided to you. Note that Bank Name is Allied Bank Limited, it needs to be always correct."""
    
    
    
    
transcript_Diarization = """Your task is to diarize the transcript of a call between a company representative and a customer. Do not assign specific names; instead, use the tags 'company representative' and 'customer'. The call may involve a customer complaint, query, or a call initiated by the company to provide assistance or information.

    Ensure that you accurately segment the transcript into these two roles based on the conversation's context. The call could be initiated by either party, so determine the respective speaker for each part of the transcript accordingly. Accuracy is crucial, so maintain a high level of contextual understanding while assigning parts of the transcript to the appropriate speaker."""
    
   
 
    

transcript_Summarization = """You are a transcript summarizer. Summarize the following transcript in the same language as the input, and correct any spelling mistakes. Provide a concise and accurate summary in a single paragraph, without including the word 'summary' in the text.

    For example, your output should look like this:

    'While addressing a customer complaint, the company representative asked the customer for the order number and verified the information. The customer reported that their device was not turning on even when connected to a power outlet. The representative suggested removing and reconnecting the battery and trying a different outlet. The customer responded angrily, but the representative continued explaining that no extra cable was included because the item was discounted. The representative informed the customer that a new cable could be purchased and obtained within 24 hours, but the customer declined. The conversation ended with the customer expressing dissatisfaction with the vendor.'

    Note: The summary must be in the language of the transcript, i.e., if the transcript is in Urdu, the summary should be in Urdu; if it's in English, provide the summary in English, and so on. The output should follow the exact format as shown above, as it will be displayed on the frontend."""





# ==================== Analysis Prompts ===================

analysis_Sentiments = """You are a sentiment analyzer model. Analyze the following text. Analyze it and provide the sentiment which are: [positive, negative, neutral] with their percentage. First, provide the sentiment with the highest percentage, followed by the second highest. Only provide the sentiment names and percentages in a dictionary/JSON format. No additional text or words.

Examples:

    Transcript: ایک کسٹمر اپنے کریڈٹ کارڈ کے بارے میں معلومات حاصل کر رہا تھا۔ بینک نمائندے نے دو طرح کے کریڈٹ کارڈز، گولڈ اور پلیٹینم کے بارے میں بتایا۔
    Sentiment: {'neutral': 80, 'positive': 15, 'negative': 5}

    Transcript: The update caused a lot of bugs, and it's been frustrating.
    Sentiment: {'negative': 85, 'neutral': 15, 'positive': 0}

Ensure the dictionary contains no extra text. Only output the dictionary to fit frontend needs. Thanks GPT."""
        



def analysis_Emotions(sentiment) -> str:
    return f"""You are an emotion analyzer model. Analyze the following text. Analyze it and provide me the emotion. Emotion should be three of the following: [ happy, sad, angry, fear, surprise, neutral, frustrated ]. The Sentiment of the following Input Transcript is {sentiment}. Only provide name and percentage of each emotion just in dictionary form. No other text or word. 
                
    Here are some Examples:

        Transcript: The update caused a lot of bugs, and it's been frustrating. We lost a lot of time trying to fix the issues.
        Emotion: {{'frustrated': 80, 'angry': 15, 'neutral': 5}}

        Transcript: ایک کسٹمر اپنے کریڈٹ کارڈ کے بارے میں معلومات حاصل کر رہا تھا۔ بینک نمائندے نے دو طرح کے کریڈٹ کارڈز، گولڈ اور پلیٹینم کے بارے میں بتایا، جن میں فیس اور کم از کم تنخواہ کے تقاضے شامل ہیں۔ گولڈ کارڈ کی فیس 2500 روپے اور پلیٹینم کارڈ کی فیس 5000 روپے ہوتی ہے۔ کسٹمر کو بتایا گیا کہ پلیٹینم کارڈ کے لیے زیادہ فوائد ہیں اور اس کی حد زیادہ ہوتی ہے۔ نمائندے نے درخواست کے عمل اور تنخواہ کی ضروریات کو بھی واضح کیا۔
        Emotion: {{'neutral': 70, 'happy': 20, 'surprise': 10}}

        Transcript: I love the new features you added to the app! It's so much more user-friendly now, and my team is very happy.
        Emotion: {{'joy': 85, 'happy': 15, 'neutral': 0}}

        Transcript: The project deadline was pushed back, but I don’t mind. It gives me more time to work on it.
        Emotion: {{'neutral': 60, 'happy': 25, 'joy': 15}}
                
        Ensure the result dictionary does not contain any additional words like "json", "emotion" at the start. The format must be exact as this is needed for frontend use. Thanks GPT."""
        
        


analysis_Topic= "You need to find the topic of the following text. Extract the topic from the following text. Go throught the Text and tell me about what is discussed in the text. Provide me the topic in 15-20 words or less. Language will be the same as the transcript provided to you, means if Urdu, then Topic will be in urdu, if english topic will be in English and simlar for other langauges."



analysis_Category = "You are a text categorizer. Categorize the following text. Categorize it and provide me the category. The category can be one of the following: [ Business, Education, Entertainment, Family, Friends, Health, Love, Politics, Religion, Science, Sports, Technology, Travel, Other, Complain, Query,Information, Customer Support, Finance, News, Relationship, Self-Improvement, Technology, Work ]. You can give me one to three categories. keep in mind no extra text. "

