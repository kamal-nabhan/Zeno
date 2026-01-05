"""
Command executor for running parsed commands
"""
from typing import Optional, List
from zeno.integrations.spotify import SpotifyIntegration
from zeno.integrations.weather import WeatherIntegration
from zeno.integrations.search import ImageSearch
from zeno.ai.base import BaseAI
from zeno.core.speech import SpeechManager


class CommandExecutor:
    """Execute commands from parsed responses"""
    
    def __init__(self, ai: BaseAI, speech: SpeechManager):
        self.ai = ai
        self.speech = speech
        
        # Initialize integrations
        self.spotify = SpotifyIntegration()
        self.weather = WeatherIntegration()
        self.image_search = ImageSearch()
    
    def execute(self, commands: List[str]) -> None:
        """
        Execute a list of commands
        
        Args:
            commands: List of command strings to execute
        """
        for command in commands:
            self._execute_single(command)
    
    def _execute_single(self, command: str) -> None:
        """
        Execute a single command
        
        Args:
            command: Command string to execute
        """
        command_lower = command.lower()
        
        # Spotify commands
        if "spotify-play" in command_lower or command_lower == "play":
            self._handle_spotify_play()
        
        elif "spotify-pause" in command_lower or command_lower == "pause":
            self._handle_spotify_pause()
        
        elif "spotify-skip" in command_lower or command_lower == "skip":
            self._handle_spotify_skip()
        
        elif "spotify-previous" in command_lower or command_lower == "previous":
            self._handle_spotify_previous()
        
        elif "spotify-info" in command_lower or command_lower == "spotify":
            self._handle_spotify_info()
        
        # Weather command
        elif "weather" in command_lower:
            self._handle_weather()
        
        # Image search command
        elif "search" in command_lower:
            query = command.split("-")[1] if "-" in command else "default"
            self._handle_image_search(query)
        
        # Device control placeholders
        elif "3d_printer" in command_lower:
            state = command.split("-")[1] if "-" in command else "0"
            self._handle_3d_printer(state)
        
        elif "lights" in command_lower:
            state = command.split("-")[1] if "-" in command else "0"
            self._handle_lights(state)
        
        else:
            print(f"Unknown command: {command}")
    
    # Spotify handlers
    def _handle_spotify_play(self) -> None:
        """Handle Spotify play command"""
        error = self.spotify.play()
        if error:
            print(f"Spotify play error: {error}")
    
    def _handle_spotify_pause(self) -> None:
        """Handle Spotify pause command"""
        error = self.spotify.pause()
        if error:
            print(f"Spotify pause error: {error}")
    
    def _handle_spotify_skip(self) -> None:
        """Handle Spotify skip command"""
        error = self.spotify.next_track()
        if error:
            print(f"Spotify skip error: {error}")
    
    def _handle_spotify_previous(self) -> None:
        """Handle Spotify previous command"""
        error = self.spotify.previous_track()
        if error:
            print(f"Spotify previous error: {error}")
    
    def _handle_spotify_info(self) -> None:
        """Handle Spotify info command - get current track and speak it"""
        track_info = self.spotify.get_current_track()
        if track_info:
            query = f"System information: {str(track_info)}"
            print(query)
            response = self.ai.ask(query)
            self.speech.speak(response)
    
    # Weather handler
    def _handle_weather(self) -> None:
        """Handle weather command"""
        weather_info = self.weather.get_weather()
        query = f"System information: {weather_info}"
        print(query)
        response = self.ai.ask(query)
        self.speech.speak(response)
    
    # Image search handler
    def _handle_image_search(self, query: str) -> None:
        """Handle image search command"""
        error = self.image_search.search(query)
        if error:
            print(f"Image search error: {error}")
        else:
            print(f"Downloaded images for: {query}")
    
    # Device control placeholders
    def _handle_3d_printer(self, state: str) -> None:
        """Handle 3D printer control (placeholder)"""
        action = "ON" if state == "1" else "OFF"
        print(f"[PLACEHOLDER] 3D Printer: {action}")
        # TODO: Implement actual 3D printer control
    
    def _handle_lights(self, state: str) -> None:
        """Handle lights control (placeholder)"""
        action = "ON" if state == "1" else "OFF"
        print(f"[PLACEHOLDER] Lights: {action}")
        # TODO: Implement actual lights control
