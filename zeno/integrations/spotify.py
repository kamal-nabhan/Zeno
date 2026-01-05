"""
Spotify integration for music control
"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import Optional, Dict
from zeno.core.config import config


class SpotifyIntegration:
    """Spotify music control integration"""
    
    def __init__(self):
        self.client: Optional[spotipy.Spotify] = None
        self._initialize()
    
    def _initialize(self) -> None:
        """Initialize Spotify client with credentials from config"""
        if not all([
            config.SPOTIFY_CLIENT_ID,
            config.SPOTIFY_CLIENT_SECRET,
            config.SPOTIFY_USERNAME
        ]):
            print("Warning: Spotify credentials not configured")
            return
        
        try:
            scope = "user-read-currently-playing user-modify-playback-state"
            auth_manager = SpotifyOAuth(
                client_id=config.SPOTIFY_CLIENT_ID,
                client_secret=config.SPOTIFY_CLIENT_SECRET,
                redirect_uri=config.SPOTIFY_REDIRECT_URI,
                scope=scope,
                username=config.SPOTIFY_USERNAME
            )
            self.client = spotipy.Spotify(auth_manager=auth_manager)
        except Exception as e:
            print(f"Failed to initialize Spotify: {str(e)}")
            self.client = None
    
    def is_available(self) -> bool:
        """Check if Spotify integration is available"""
        return self.client is not None
    
    def get_current_track(self) -> Optional[Dict[str, str]]:
        """
        Get information about the currently playing track
        
        Returns:
            Dictionary with artist, album, and title, or None if nothing is playing
        """
        if not self.is_available():
            return {"error": "Spotify not configured"}
        
        try:
            current_track = self.client.current_user_playing_track()
            if current_track is None:
                return None
            
            return {
                "artist": current_track['item']['artists'][0]['name'],
                "album": current_track['item']['album']['name'],
                "title": current_track['item']['name']
            }
        except spotipy.SpotifyException as e:
            return {"error": f"Spotify error: {str(e)}"}
    
    def play(self) -> Optional[str]:
        """Start or resume playback"""
        if not self.is_available():
            return "Spotify not configured"
        
        try:
            self.client.start_playback()
            return None
        except spotipy.SpotifyException as e:
            return f"Error starting playback: {str(e)}"
    
    def pause(self) -> Optional[str]:
        """Pause playback"""
        if not self.is_available():
            return "Spotify not configured"
        
        try:
            self.client.pause_playback()
            return None
        except spotipy.SpotifyException as e:
            return f"Error pausing playback: {str(e)}"
    
    def next_track(self) -> Optional[str]:
        """Skip to next track"""
        if not self.is_available():
            return "Spotify not configured"
        
        try:
            self.client.next_track()
            return None
        except spotipy.SpotifyException as e:
            return f"Error skipping track: {str(e)}"
    
    def previous_track(self) -> Optional[str]:
        """Go to previous track"""
        if not self.is_available():
            return "Spotify not configured"
        
        try:
            self.client.previous_track()
            return None
        except spotipy.SpotifyException as e:
            return f"Error going to previous track: {str(e)}"
