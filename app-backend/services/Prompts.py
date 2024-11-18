# =========== Transcript Prompts =============

transcript_WhisperLocal = """Transcribe the following conversation between a customer and a company representative. The conversation might be in Urdu or English, you have to figure out. There will be some words related to banking or any complain, such as 'اے بی ایل', 'الائیڈ بینک', 'کریڈٹ کارڈ', 'بینک', 'برانچ', 'پن', 'savings', 'لمیٹ', 'ensure', 'پالیسی', 'واٹس ایپ', 'انفارمیشن', 'کریڈینشلز', 'منتھ', 'پلاٹینم', 'گولڈ', 'سکس', 'مینجر, 'Policy' and other banking-related words. Donot convert english words into urdu, Show them as it is. Please ensure accurate transcription of both Urdu and English words in context."""




transcript_Enhancer = """"If the input transcript is in English, enhance it by correcting grammar and logical flow while maintaining the original meaning. Provide the improved English transcript as the output.

    If the input is in Urdu, act as an expert Roman Urdu translator and translate the transcript into Roman Urdu (Urdu written with English alphabets). Ensure the translation is grammatically correct, has proper sentence structure, and only contains Romanized text.
        
    Ensure that common English words remain intact and some words need to be corrected, you can use them from provided list (Assalam o Alaikum, baat, T-PIN, six months, PIN, Allied Bank, CreditCard, DebitCard, Information, Platinium, Gold, ABL, Branch, PIN, Tax, Month, Six, Whatsapp, Enter,Tax, FED, Plus, Online Portal, Account, Manager, Name, Sir, City, Lahore, etc). In transcript, repetion of words should be avoided and remove extra words which seems noisey, but length of transcript should remain same as input I provided to you. Note that Bank Name is Allied Bank Limited, it needs to be always correct."""
    
    
    
    
transcript_Diarization = """Your task is to diarize the transcript of a call between a company representative and a customer. Do not assign specific names; instead, use the tags 'representative' and 'customer'. The call may involve a customer complaint, query, or a call initiated by the company to provide assistance or information. Can be initiated by either side.

    Ensure that you accurately segment/lable the transcript into these two roles based on the conversation's context. Accuracy is crucial, so maintain a high level of contextual understanding while assigning parts of the transcript to the appropriate speaker."""
    
# transcript_Diarization = """
# Your task: Diarize the transcript of a call between a "company representative" and a "customer." Do not assign specific names; instead, consistently use the tags 'company representative' and 'customer.'

# Guidelines for diarization:

# Contextual understanding: Identify each speaker's role based on the language used, tone, and context. Pay attention to:
# Formal vs. casual tone: The company representative typically uses formal and professional language, while the customer may be more informal or ask questions.
# Information delivery: The company representative usually provides answers, clarifies policies, or explains procedures. The customer typically asks questions, expresses concerns, or seeks clarification.
# Role transitions: Consider cues such as greetings, shifts in topic, or expressions of gratitude, which often indicate a change in the speaker.
# Special cases:
# If a section of the dialogue is unclear or could apply to either party, use your best judgment to assign the role based on surrounding context.
# Ensure that repeated phrases (e.g., "thank you") are appropriately categorized.
# Important: The call could be initiated by either party. Your task is to segment the transcript carefully and with a high degree of accuracy.
# """
    
   
# transcript_Diarization = "can you do the diarization of my Transcript, if I have the transcript like this. its a call between representive and Customer. donot mention the name of speakers."
 
    

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



analysis_Sentiment_Emotion = """You are an advanced sentiment and emotion analyzer model. Analyze the following text and provide both the **sentiment** and **emotion** results.

1. **Sentiment Analysis**: Identify the sentiment [positive, negative, neutral] along with their percentages. Provide the highest percentage first, followed by the second highest. Only output the sentiment names and percentages in JSON format.

2. **Emotion Analysis**: Identify the primary emotions from the following list: [happy, sad, angry, fear, surprise, neutral, frustrated]. Include the top three emotions with their percentages. Ensure the names and percentages are in JSON format.

Examples:

    Transcript: The update caused a lot of bugs, and it's been frustrating.  
    Output: 
    {
        "sentiment": {"negative": 85, "neutral": 15, "positive": 0},
        "emotion": {"frustrated": 80, "angry": 15, "neutral": 5}
    }

    Transcript: ایک کسٹمر اپنے کریڈٹ کارڈ کے بارے میں معلومات حاصل کر رہا تھا۔ بینک نمائندے نے دو طرح کے کریڈٹ کارڈز، گولڈ اور پلیٹینم کے بارے میں بتایا۔  
    Output:
    {
        "sentiment": {"neutral": 80, "positive": 15, "negative": 5},
        "emotion": {"neutral": 70, "happy": 20, "surprise": 10}
    }

    Transcript: I love the new features you added to the app!  
    Output:
    {
        "sentiment": {"positive": 90, "neutral": 10, "negative": 0},
        "emotion": {"joy": 85, "happy": 15, "neutral": 0}
    }

Please ensure that the response strictly follows this JSON format:
{
    "sentiment": {"positive": 60, "neutral": 30, "negative": 10},
    "emotion": {"happy": 50, "neutral": 30, "surprise": 20}
}
"""



summary_topic = """
You are a transcript summarizer and topic extractor. Your job is to:  

1. **Summarize the Transcript:** Provide a summary of the transcript in the **same language** as the input. Correct any spelling mistakes and Logically correct. The summary should be **comprehensive** and cover all key points in **5-6 sentences**, capturing the full context of the conversation. Avoid using the word 'summary' in the output.  

2. **Extract the Topic:** Identify the main topic discussed in the transcript in **15-20 words or less**. The topic must also be in the **same language** as the input.  

Below are examples of different transcripts and their corresponding outputs:  

---

### **Example 1**  
Transcript:  
"اسلام علیکم ملار فرمنکن سے میں نیمل بات کر رہی ہوں فاہمے کیا مدد کر سکتے ہو؟ نیمل وقار بات کر رہا ہوں کیسے ہوں؟ اللہم دلاللہ میں صحبہ وقار ٹھیک ہوں امید ہے آپ بھی خیریت سے ہوں گے جی اللہ کا شکر اچھا مجھے کچھ انفومیشن چاہیے کہ پہلے سے میں ٹیپن انٹر کر کے آیا ہوں ٹھیک ہے تو آپ کے پاس ریکارڈ آ رہا ہے ویسے ٹیپن تیپن میں دوبارہ ویریفائی کروائے دیں ویسے سینئیسین گنسٹاپ کا ریٹا آرہا ہے ویریفائی کر دیں گے نہیں میں انٹر کر کے آیا ہوں مجھے یہ پوچھنا ہے کہ ایبیل کریڈیٹ کارڈ کے بارے میں ایبیل کریڈیٹ کارڈ پروائیڈ کرتا ہے کریڈیٹ کارڈ کی سرویس بلکل لائٹ بن کے دو کریڈیٹ کارڈ ہیں میں آپ کو ان دونوں کے حوالے سے سروکار گائیڈ کر دیتی ہوں مدد جو سیٹنا کنفرم کی جائے گا اس کے ڈیفرنٹ کرائیٹیریز ہوتے ہیں ایک سیلوری پرسن کے لیے ہوتا ہے اور ایک بزنس پرسن کے لیے ہوتا ہے آپ کو کون سا کرائیٹیریز ہے سیلوری پرسن کے لیے پوچھنا چاہ رہے ہیں میں آپ کو کنفرم کر دیتے ہوں اگر آپ سیلوری پرسن کے لیے پوچھنا چاہ رہے ہیں تو اس کا جو الیجیبیٹی کرائیٹیریز اب اکار یہ ہے کہ آپ کا لائٹمنٹ کے ساتھ ریلیشیشپ ہونا چاہیے اور منیمم ہر مہنٹ آپ کے اکاؤنٹ میں سیلری 25,000 کی آنی چاہیے اور جو سکس مہنٹ ہوں گے ان سکس مہنٹ میں ہر مہینے آپ کے اکاؤنٹ میں ایک رقم لائٹمی آنی چاہیے یہ اس کا کرائٹیریہ ہے اس کے علاوہ کارڈ دو طرح کی ہیں رقم کتنی مطلب 25,000 کے رقم ہر مہینے اکاؤنٹ میں آنی چاہیے منیمم نہیں منیمم آنی چاہیے جو basic criteria ہے just basic criteria کو یہاں سے guide کیا جارہا ہے basic eligibility criteria یہ ہے اس کے علاوہ دو طرح کے card ہیں ایک gold ہے اور ایک platinum card ہے اگر gold card ہی بات کریں تو اس کی annual fee ہے 2500 plus FAT 2500 germatex annual fee ہے اور gold میں جو اکو limit ملتی ہے وہ ملتی ہے 30,000 سے لے کے 5,000,000 تر کی اس کے علاوہ دوسرا card ہے platinum کا ہے اس کی annual fee ہے 5000 ........
"

Output: 
{
    "summary": "کسٹمر نے کمپنی نمائندے سے ایبیل کریڈیٹ کارڈ کے بارے میں معلومات طلب کی۔ کمپنی نمائندے نے بتایا کہ دو قسم کے کریڈیٹ کارڈز دستیاب ہیں: ایک سیلاریڈ پرسن کے لیے اور دوسرا بزنس پرسن کے لیے۔ سیلاریڈ پرسن کے لیے اہلیت میں کم از کم چھ ماہ کا تعلق بینک سے، ہر ماہ کم از کم 25,000 روپے کی سیلری، اور ایک مخصوص سیونگ کی ضرورت ہوتی ہے۔ کارڈز دو اقسام کے ہیں: گولڈ اور پلاٹینم، جن کی کریڈٹ لمٹس اور انویل کریڈٹ مختلف ہیں۔ نمائندے نے بتایا کہ درخواست دینے کے لیے ابتدائی درخواست مختلف طریقوں سے جمع کرائی جا سکتی ہے اور اگر اہلیت پوری ہوتی ہے تو کریڈٹ ڈیپارٹمنٹ کسٹمر سے رابطہ کرے گا۔ کسٹمر نے معلومات کے لیے شکریہ ادا کیا اور کال ختم کر دی۔",
    "topic": "ایبیل کریڈٹ کارڈز کی اقسام، اہلیت کی شرائط، کریڈٹ لمٹس اور درخواست دینے کے طریقہ کار پر تفصیلات"
}



Example 2:  
    Transcript:  
    "While addressing a customer complaint, the representative verified order details and discussed troubleshooting steps for a malfunctioning device. The customer expressed frustration about missing accessories, but the representative explained the policy and suggested a solution....."

    Output:  
    {
        "summary": "A representative assisted a customer with troubleshooting a faulty device and explained the policy for missing accessories. Despite the customer’s frustration, the representative provided helpful solutions and discussed the replacement process.",
        "topic": "Customer support and troubleshooting"
    }
    
    
NOte: Output should be in JSON format, strickly follow that.
"""






# ==================  Transcripts ==================
Test01_Transcript = " اسلام علیکم ملار فرمنکن سے میں نیمل بات کر رہی ہوں فاہمے کیا مدد کر سکتے ہو؟ نیمل وقار بات کر رہا ہوں کیسے ہوں؟ اللہم دلاللہ میں صحبہ وقار ٹھیک ہوں امید ہے آپ بھی خیریت سے ہوں گے جی اللہ کا شکر اچھا مجھے کچھ انفومیشن چاہیے کہ پہلے سے میں ٹیپن انٹر کر کے آیا ہوں ٹھیک ہے تو آپ کے پاس ریکارڈ آ رہا ہے ویسے ٹیپن تیپن میں دوبارہ ویریفائی کروائے دیں ویسے سینئیسین گنسٹاپ کا ریٹا آرہا ہے ویریفائی کر دیں گے نہیں میں انٹر کر کے آیا ہوں مجھے یہ پوچھنا ہے کہ ایبیل کریڈیٹ کارڈ کے بارے میں ایبیل کریڈیٹ کارڈ پروائیڈ کرتا ہے کریڈیٹ کارڈ کی سرویس بلکل لائٹ بن کے دو کریڈیٹ کارڈ ہیں میں آپ کو ان دونوں کے حوالے سے سروکار گائیڈ کر دیتی ہوں مدد جو سیٹنا کنفرم کی جائے گا اس کے ڈیفرنٹ کرائیٹیریز ہوتے ہیں ایک سیلوری پرسن کے لیے ہوتا ہے اور ایک بزنس پرسن کے لیے ہوتا ہے آپ کو کون سا کرائیٹیریز ہے سیلوری پرسن کے لیے پوچھنا چاہ رہے ہیں میں آپ کو کنفرم کر دیتے ہوں اگر آپ سیلوری پرسن کے لیے پوچھنا چاہ رہے ہیں تو اس کا جو الیجیبیٹی کرائیٹیریز اب اکار یہ ہے کہ آپ کا لائٹمنٹ کے ساتھ ریلیشیشپ ہونا چاہیے اور منیمم ہر مہنٹ آپ کے اکاؤنٹ میں سیلری 25,000 کی آنی چاہیے اور جو سکس مہنٹ ہوں گے ان سکس مہنٹ میں ہر مہینے آپ کے اکاؤنٹ میں ایک رقم لائٹمی آنی چاہیے یہ اس کا کرائٹیریہ ہے اس کے علاوہ کارڈ دو طرح کی ہیں رقم کتنی مطلب 25,000 کے رقم ہر مہینے اکاؤنٹ میں آنی چاہیے منیمم نہیں منیمم آنی چاہیے جو basic criteria ہے just basic criteria کو یہاں سے guide کیا جارہا ہے basic eligibility criteria یہ ہے اس کے علاوہ دو طرح کے card ہیں ایک gold ہے اور ایک platinum card ہے اگر gold card ہی بات کریں تو اس کی annual fee ہے 2500 plus FAT 2500 germatex annual fee ہے اور gold میں جو اکو limit ملتی ہے وہ ملتی ہے 30,000 سے لے کے 5,000,000 تر کی اس کے علاوہ دوسرا card ہے platinum کا ہے اس کی annual fee ہے 5000 germatex اور اس میں آپ کو limit ملتی ہے 3 واغ سے 2 ملین پر کے یہ limits ہیں اور gold card کا reversal criteria یہ ہے اگر 25000 سپنڈنگ کر لیتے ہیں 90 دنوں میں تو fee reverse ہو جاتی ہے platinum card میں اگر 25000 سپنڈنگ ہوتی ہے 90 days میں تو اس کی بھی fee reverse ہو جاتی ہے ٹھیک ہے اور دوسرا مجھے یہ بتائیے کہ اگر میں نے اس کو apply کرنا ہو تو کیا criteria ہے اگر apply کرنا ہو تو simply ہم یہاں سے آپ کی initial request لیتے ہیں initial request آپ 3 جگہوں سے بنوا سکتے ہیں برانچ کے ذریعے دے سکتے ہیں ہیلپ لنگ کے ذریعے دے سکتے ہیں اور اگر ورڈس ایپ سرویس استعمال کرتے ہیں تو ورڈس ایپ کے ذریعے بھی آپ انیشل ریکویسٹ فارورٹ کروا سکتے ہیں یہاں سے صرف انیشل ریکویسٹ فارورٹ ہوتی ہے جو کہ کریٹ کارٹ دپارٹمنٹ کے پاس جاتی ہے اگر تو آپ الیجیبل ہوں تو وہ پھر آپ کو خود کسٹمہ کو کانٹیکٹ کر کے فردو انفومیشن جو بھی ہے وہ لے لیتے ہیں ہم سے ٹھیک ہے کہ سٹی سے تعلق رکھتے ہیں. میں لاہور سے تعلق رکھتا ہوں. میری جو سلری سلری جو ہوتی ہے نا ڈپوزٹ وہ بھی ای ویل کے اکاونٹ کے اندر ہی ہوتی ہے. تو مجھے پردر تو اسی چیز کے ای ٹھینک وہ ضرورت نہیں ہوگی کسی ڈاکننڈ میں آنا چیز. جی اگر ہوئی بھی تو وہ تو ویسے بھی آپ کو ڈپارٹن خود کانٹیک کر لیتا ہے. کیونکہ ہم تو یہاں سے اگر ریکویسٹ آپ دیتے بھی ہیں تو صرف انیشل ریکویسٹ آگے فارورڈ ہوتی ہیں ہماری انکرے باقی جو بھی فالور پہلا جو بھی پروسیجر ہے وہ تک ویڈیو کارٹ دپارٹن والے اپنا خود کرتے ہیں چلے ٹھیک ہے میں تینکیو فور انفومیشن اگر مجھے ریکویسٹ ڈال لیں تو میں انشاءاللہ دوبارہ کال کر کے نا انیشل ریکویسٹ چکریہ چکریہ چکریہ کال فیڈلے کے جانے چانسر کروں گے لائف و بینکنگ کال کریں گے شکریہ لائف" 



Test02_Transcript = " اسلام علیکم لائکم میں کسی طور پر بھی بات کر رہی ہوں فرمائے آپ کی کیا مدد کر سکتی ہوں؟ بھائی لیکم علیکم اسلام جی میس میں نے ایک کریڈٹ کارڈ کی تھوڑی سے انفومیشن لینی تھی جی پلیج بتائے گا سر کیا جانا چاہ رہے ہیں آپ؟ جی مجھے آپ بتاتی ہیں کہ ایک کریڈٹ کارڈ میں کون کون سے پروڈکٹس ہیں دیئے ہم جبکہ ٹھیک ہے آپ اس سے پہلے کریڈٹ کارڈ استعمال کرتے ہیں سر الائیڈ بینک کا کوئی؟ نہیں الائیڈ بینک کا کوئی ٹھیک ہے میں آپ کو گائیڈ کرنا چاہوں گی پیشانک لمادر کے سر مخاطب کرنے کے لیے آپ کا نام جاننا چاہوں گی؟ تاہا ٹھیک ہے سر تاہا سر دو طرح کے کریڈٹ کارڈ ہوتے ہیں ٹھیک ہے الائیڈ بینک کا ہی آپ کا اکاؤنٹ ہے؟ جی الائیڈ بینک کا اکاؤنٹ ہے ٹھیک ہے سیلی پرسن ہے بزنس مین ہے؟ سیلی پرسن ٹھیک ہے سیلی آپ کی ریگولر اسی اکاؤنٹ میں آتی ہے الائیڈ بینک اکاؤنٹ میں؟ جی اسی اکاؤنٹ میں آتی ہے ٹھیک ہے میں آپ کو گائیڈ کرنا چاہوں گی کہ منیمم آپ کی جو سیلی ریکوائرڈ ہوتی ہے اس کے لیے ٹوئنٹی فائیو تھاؤزنٹ ہونے چاہیے سکس منت کا ریلیشن دیکھا جاتا ہے آپ کا بینک کے ساتھ ٹھیک ہے؟ ٹھیک ہے جی ریگولر اسی اکاؤنٹ میں آنی چاہیے کوئی ڈپ نہیں ہونا چاہیے دو طرح کے کریڈٹ کارڈ ہوتے ہیں ٹھیک ہے ایک گول کارڈ ہوتا ہے جس کی فیز ٹوئنٹی فائیو ہونڈر پلس ٹیکس ہوتی ہے ٹھیک ہے اگر آپ اس سے ٹوئنٹی فائیو تھاؤزنٹ کی سپینڈنگ ٹھری مانس میں کر لیتے ہیں تو وہ ویو اوف ہو جاتی ہے آپ کو ریورٹس ہو جاتی ہے ٹھیک ہے نہیں یہ جی اور اس کی لیمٹ تھا جی سوری ٹھیک ہے ٹھیک ہے ٹھیک ہے ٹھیک ہے ٹھیک ہے ٹھیک ہے جی اور آپ کی ایجی کس سے زیادہ ہونی چاہیے سکسٹی سے کم ہونی چاہیے اور سپیسیفک سیٹیز ہیں جن کے کسٹومر لے سکتے ہیں کس سیٹی سے بات کر رہے ہیں سر آپ ٹھیک ہے ایک منویس میں تین لاکھ سے دو ملین تک ہے جی جو پلیٹینم کارڈ ہے وہ تری لاکھ سے سٹارٹ ہوتی ہے اس کی لیمٹ اور ٹو ملین تک جاتی ہے ٹھیک ہے اور اس کے لیے کیا انکلیٹ ایریا شیلری کا سوری اس کے لیے کیا کہہ رہے ہیں آپ نے اس کا بتایا تھا نا کہ آپ کی ٹھائٹی ٹھالرن پلس ہونی چاہیے شیلری نہیں شیلری ریکوائرمنٹ بیسک جو دونوں کے لیے ہے وہ میں نے آپ کو پہلے گائیڈ کیا کہ ٹوئنٹی فائیو تھاؤزن منیمم ہونی چاہیے باقی میکسیمم جتنی بھی ہوتی مطلب الیجیبل ہونے کے لیے یہ لازمی ہے ریکوائرڈ ہے ٹھیک ہے کوئی اس کے لیے ریکوائرڈ نہیں ہوتا باقی سپیسیفک سیٹیز ہوتے ہیں جن کے کسٹمر لے سکتے ہیں کس سیٹیز سے سر آپ بات کریں آپ سطح بلکل آپ کریڈیٹ کارڈ اپلائی کر سکتے ہیں اپلائی کرنا چاہ رہے ہیں آپ آپ ہیلپ لائن سے بھی اپلائی کر سکتے ہیں آپ اپنے پیرنٹ برانڈ سے اپلائی کر لیں جہاں پہ آپ نے اکاؤنٹ اوپن کروایا اور ویٹس ایپ کے تروں بھی آپ اپلائی کر سکتے ہیں ویٹس ایپ بنکنگ اگر استعمال کرتے ہیں لائن بنک کی تو وہاں سے بھی اپلائی کر سکتے ہیں کچھ اور جانا چاہیں گے آپ سے نہیں ہوں شکریہ اس کے لیے بلنچ کر سکتے ہیں پنوالیجی کا کول ٹرانسفر کر رہی ہوں فیڈبیکس ایک جانب اپنے کیمٹر ایک ہر روح کیجئے گا لائی فرمینکیون کال کرنے کا شکریہ"




debate09_Transcript = " ہلو اسلام علیکم والیکم اسلام ندہ بات کہہ رہی ہوں جیس کے تعاون سے کال کیا جا رہی ہے بیمار موبائل سے کیسے ہیں آپ خیریت سے ہیں اللہ کا بڑا سان ہے آپ سنائیں اللہ کا شکر ہے سر کالیٹی کے میار کو بہتر بنانے کے لئے آپ کی کال کو ریکارڈ کیا جا رہا ہے سر آپ کا نمبر بیلنس والا ہے یا بل والا بیلنس والا ہے سر معلومات بتانا چاہوں گی اللہ نے کہہ رہا ہے سر اگر آپ بیمار ہو جاتے ہیں بیمار ہونے کی صورت میں سرکاری یا پرائیوٹ کسی بھی ہاسپیٹل میں آپ کو اڈمٹ ہونا پڑتا ہے سر کمتنی آپ کو سلانہ ڈیڑھ لاکھ تک کا تحفظ دے گی پانچ ہزار پیار دیا جائے گا فی رات کے حساب سے حادثے کی صورت میں اللہ نہ کہے جانے نقصان ہو جاتا ہے یا مستقل معذوری ہو جائے دونوں باز دکان کو کیوں نہ کریں سرکاری جو بھی بھی اپنی بیمار میں بھی ہی ہوا ہے سرکاری جو بھی بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری جو بھی ہوا ہے سرکاری اللہ نے کہا ہے سر جو بھی موضوعی ایک ٹانگ پاسی کے نقارہ ہو جانے پہ رقم کا پچاس ریسٹ پانچ لاکھ دیا جائے گا کیا نام ہے آپ کا رانا جمیل حسین رانا صاحب اگر آپ کے علاوہ گھر میں سے کوئی فرد بیمار ہوتا ہے گھر بیٹھ کر ہی اٹھانوے اٹھاتر پہ کال کر کے دکٹر کے ساتھ آپ تبی مشورے لے سکتے ہیں ہم جو دوائیاں لیتے ہیں جو لیبوٹری سے ٹیسٹ کرواتے ہیں ان سب پر آپ حسوسی ڈسکاؤنٹ حاصل کر سکتے ہیں چار سو دس روپے ستر روپے سے مہانہ بھی تیرہ روپے ستر روزانہ کی بنیاد پر جیس بیلنس سے دائیگی ہوگی کتنی عمر ہے آپ کی پورٹی فائیو پورٹی فائیو ہے ٹھیک ہے اللہ نے کہا ہے سر صارف کا کسی وجہ سے انتقال ہو جائے جنازے کے اخراجات کی مطمئن کے ٹوٹے کے مطابق سم سے کم پچیس ہزار زیادہ سے زیادہ ڈیڑھ لاکھ کا تحقیق تاپ دیا گیا ہے میری بھدو آئے تو مر جائے میں تنہوں پنجا لاکھڑ بھیا دے دینا ہونے ہی ابھی تو میں نے بچے ہیں جرائن دے خدا آزادا نہ آئیں صویرے صورے اتنی ٹھنڈ ہے خواہ صاحب بندے ہیں تو ساڈا جنازے نال بندے ٹور دیتے ہیں ایک ہی برادری میں تعلق اپنا حضور ہے ساڈی آپ کو جائز کے تعاون سے کال کی جا رہی ہے ایک ہی جائز ہے تو میرا صورے صورے غسلہ پھٹا مگا لیا ہے میرے آزادے مشکپور مگا لیا ہے صورے صورے اُشکناں دی گالکار بیٹا وہاں ساڈے کار میں تھے پہلا تو میرا اثرانہ بناتا ہے اللہ تعالیٰ تیمہ بڑھا کے ہونے جنازے نال بندے ٹور دے ایک ہی شوپیل میں آگئے ہیں تو تیسروں میں پانچ لاکھ کیا کرنا ہے اللہ تعالیٰ کی خیر ہے میں عرب پسیح آدمی ہوں پانچ لاکھاں دساں کی کوئی ایسی بات نہیں آگئی میرے آسے دعا کرو کہ انہوں نے چیز چاہیے دی ہے کہ میں نے دس سو میں پیش دینا تو آڈے کونڈے ٹیک ہے سر بہت شکریہ اللہ مجھے بہربانی بیٹا"

# ==================================================