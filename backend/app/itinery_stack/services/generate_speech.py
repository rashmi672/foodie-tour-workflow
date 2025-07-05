from groq import Groq
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
OUTPUT_DIR = os.getenv("OUTPUT_DIR")

client = Groq()

def speech_generation(text: str) -> str:
    """
    Generate speech from the given text using Groq PlayAI TTS and save it to a file.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = Path(OUTPUT_DIR) / "output.wav"
    try:
        response = client.audio.speech.create(
            model="playai-tts",
            voice="Aaliyah-PlayAI",
            response_format="wav",
            input=text,
        )
        # Correct way to save the binary content
        with open(output_path, "wb") as f:
            for chunk in response.iter_bytes():
                f.write(chunk)

        print(f"Saved synthesized speech to {output_path}")
        return str(output_path)

    except Exception as e:
        print(f"[ERROR] Speech generation failed: {e}")
        return ""
