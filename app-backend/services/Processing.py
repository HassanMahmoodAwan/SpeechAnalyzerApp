import librosa
import noisereduce as nr 
import soundfile as sf
import os
import datetime


DATASET_DIR = os.path.join(os.getcwd(), "Dataset", "sourceFiles")
OUTPUT_DIR = os.path.join(os.getcwd(), "Dataset", "processedFiles")


def preprocessing_audio(filename: str) -> str:
    audio_path = os.path.join(DATASET_DIR, filename)
    try:
        y, sr = librosa.load(audio_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    y_reduced_noise = nr.reduce_noise(y=y, sr=sr)
    
    # Get the Time Duration.
    minutes:int = int(librosa.get_duration(y=y, sr=sr) // 60)
    seconds:int = int(librosa.get_duration(y=y, sr=sr) % 60)
    timeDuration = str(round((float(f"{minutes}.{seconds}")), 2))
    
    # Get Creation-Time
    creationTime = os.path.getctime(audio_path)
    creation_time_readable = datetime.datetime.fromtimestamp(creationTime)
    time = creation_time_readable.time().replace(microsecond=0)
    date = creation_time_readable.date()
    creationTime = str(date) + " "+ str(time)
 
    # Final-audio.wav Path
    output_path = os.path.join(OUTPUT_DIR, "final_audio.wav")
    sf.write(output_path, y_reduced_noise, sr)
    
    return creationTime, timeDuration, output_path

