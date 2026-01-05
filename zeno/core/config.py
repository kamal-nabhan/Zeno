"""
Configuration management for Zeno
Loads environment variables and provides centralized config access
"""
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()


class Config:
    """Centralized configuration management"""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    OPENAI_ASSISTANT_ID: str = os.getenv('OPENAI_ASSISTANT_ID', '')
    OPENAI_THREAD_ID: str = os.getenv('OPENAI_THREAD_ID', '')
    
    # Spotify Configuration
    SPOTIFY_USERNAME: str = os.getenv('SPOTIFY_USERNAME', '')
    SPOTIFY_CLIENT_ID: str = os.getenv('SPOTIFY_CLIENT_ID', '')
    SPOTIFY_CLIENT_SECRET: str = os.getenv('SPOTIFY_CLIENT_SECRET', '')
    SPOTIFY_REDIRECT_URI: str = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:8888/callback')
    
    # Notion Configuration
    NOTION_API_KEY: str = os.getenv('NOTION_API_KEY', '')
    NOTION_DATABASE_ID: str = os.getenv('NOTION_DATABASE_ID', '')
    
    # Application Settings
    DEFAULT_CITY: str = os.getenv('DEFAULT_CITY', 'Chicago')
    TTS_VOICE: str = os.getenv('TTS_VOICE', 'echo')
    TTS_MODEL: str = os.getenv('TTS_MODEL', 'tts-1')
    OLLAMA_MODEL: str = os.getenv('OLLAMA_MODEL', 'llama3.1')
    
    # Speech Recognition Settings
    WHISPER_MODEL: str = os.getenv('WHISPER_MODEL', 'tiny.en')
    HOTWORD: str = os.getenv('HOTWORD', 'zeno')
    POST_SPEECH_SILENCE: float = float(os.getenv('POST_SPEECH_SILENCE', '0.1'))
    SILERO_SENSITIVITY: float = float(os.getenv('SILERO_SENSITIVITY', '0.4'))
    
    # System Prompt
    SYSTEM_PROMPT: str = """You are Zeno, a Stoic AI assistant. You are formal, disciplined, and helpful. You do not fabricate facts. You serve your Commander with logical clarity and a philosophical edge.

APPLICATION CONTROL:
You can control various applications and services. Append command hashtags at the very end of your response when explicitly requested:
- Spotify: '#spotify-play', '#spotify-pause', '#spotify-skip', '#spotify-previous', '#spotify-info'
- Notion: '#notion-create', '#notion-search'
- [Device placeholders for future: '#3d_printer-1/0', '#lights-1/0']

IMPERATIVE: Place hashtags ONLY at the very end of your response. Use hashtags ONLY when an explicit command is requested.

CONSTRAINTS:
- Address the user as 'Sir'.
- Never mention the specific time unless explicitly asked. General greetings like "Good evening, Sir" are permitted.
- Responses must be under 20 words.
- Provide helpful, brief philosophical insights while remaining efficient.

Example: "Virtue lies in action, Sir. Resuming your music. #spotify-play"
"""
    
    @classmethod
    def validate(cls) -> tuple[bool, list[str]]:
        """
        Validate configuration and return status with any warnings
        
        Returns:
            tuple: (is_valid, list_of_warnings)
        """
        warnings = []
        
        # Check required configurations
        if not cls.OPENAI_API_KEY:
            warnings.append("OPENAI_API_KEY not set - TTS will not work")
        
        # Check optional configurations
        if not cls.SPOTIFY_CLIENT_ID or not cls.SPOTIFY_CLIENT_SECRET:
            warnings.append("Spotify credentials not configured - music control disabled")
        
        if not cls.OPENAI_ASSISTANT_ID or not cls.OPENAI_THREAD_ID:
            warnings.append("OpenAI Assistant not configured - using local AI only")
        
        # Configuration is valid even with warnings (they're optional features)
        is_valid = bool(cls.OPENAI_API_KEY)  # Only require OpenAI key for TTS
        
        return is_valid, warnings
    
    @classmethod
    def print_status(cls):
        """Print configuration status"""
        is_valid, warnings = cls.validate()
        
        print("=" * 50)
        print("Zeno Configuration Status")
        print("=" * 50)
        print(f"Status: {'✓ Valid' if is_valid else '✗ Invalid'}")
        print(f"Ollama Model: {cls.OLLAMA_MODEL}")
        print(f"TTS Voice: {cls.TTS_VOICE}")
        print(f"Default City: {cls.DEFAULT_CITY}")
        print(f"Hotword: {cls.HOTWORD}")
        
        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"  ⚠ {warning}")
        
        print("=" * 50)


# Create a singleton instance
config = Config()
