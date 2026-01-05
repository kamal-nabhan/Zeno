"""
Command parser for extracting commands from AI responses
"""
from typing import Tuple, Optional, List


class CommandParser:
    """Parse commands from AI responses"""
    
    @staticmethod
    def parse(response: str) -> Tuple[str, Optional[List[str]]]:
        """
        Parse a response into speech text and commands
        
        Args:
            response: The AI's response
            
        Returns:
            Tuple of (speech_text, list_of_commands or None)
        """
        # Split on # to separate speech from commands
        parts = response.split('#')
        
        # First part is always the speech
        speech = parts[0].strip()
        
        # Remaining parts are commands (if any)
        commands = None
        if len(parts) > 1:
            commands = [cmd.strip() for cmd in parts[1:] if cmd.strip()]
        
        return speech, commands
    
    @staticmethod
    def has_question(response: str) -> bool:
        """
        Check if response contains a question
        
        Args:
            response: The AI's response
            
        Returns:
            True if response contains a question mark
        """
        return '?' in response
