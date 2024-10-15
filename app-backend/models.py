from sqlalchemy import Column, Integer, String, Text
from database import Base

class Speech_Analysis_Table(Base):
    __tablename__ = 'speech_analysis_table'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String, index=True)
    file_extension = Column(String)
    file_duration = Column(String)
    transcript = Column(Text)
    summary = Column(Text)
    translated_transcript = Column(Text)
    diarized_transcript = Column(Text)
    sentiment = Column(Text)
    emotion = Column(Text)
    topic = Column(String)
    category = Column(Text)