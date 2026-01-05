"""
Speech recognition and text-to-speech management
"""
from openai import OpenAI
from pygame import mixer
import os
import time
from typing import Optional
from zeno.core.config import config


class SpeechManager:
    """Manages TTS generation and audio playback"""
    
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        mixer.init()
    
    def generate_tts(self, text: str, output_path: str = "speech.mp3") -> str:
        """
        Generate speech from text using OpenAI TTS
        
        Args:
            text: Text to convert to speech
            output_path: Path to save the audio file
            
        Returns:
            Path to the generated audio file
        """
        response = self.client.audio.speech.create(
            model=config.TTS_MODEL,
            voice=config.TTS_VOICE,
            input=text
        )
        response.stream_to_file(output_path)
        return output_path
    
    def play_audio(self, file_path: str) -> None:
        """
        Play an audio file
        
        Args:
            file_path: Path to the audio file to play
        """
        mixer.music.load(file_path)
        mixer.music.play()
        
        # Wait for playback to complete
        while mixer.music.get_busy():
            time.sleep(0.1)
        
        mixer.music.unload()
    
    def speak(self, text: str, cleanup: bool = True) -> None:
        """
        Generate speech and play it
        
        Args:
            text: Text to speak
            cleanup: Whether to delete the audio file after playing
        """
        speech_file = self.generate_tts(text)
        self.play_audio(speech_file)
        
        if cleanup and os.path.exists(speech_file):
            os.remove(speech_file)
    
    def cleanup(self) -> None:
        """Cleanup resources"""
        try:
            mixer.music.unload()
        except:
            pass
