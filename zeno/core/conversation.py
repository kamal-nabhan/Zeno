"""
Conversation history management
"""
from typing import List, Dict
from datetime import datetime


class ConversationManager:
    """Manages conversation history and context"""
    
    def __init__(self):
        self.history: List[Dict[str, str]] = []
        self.max_history: int = 50  # Keep last 50 exchanges
    
    def add_user_message(self, message: str) -> None:
        """Add a user message to history"""
        self.history.append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now().isoformat()
        })
        self._trim_history()
    
    def add_assistant_message(self, message: str) -> None:
        """Add an assistant message to history"""
        self.history.append({
            'role': 'assistant',
            'content': message,
            'timestamp': datetime.now().isoformat()
        })
        self._trim_history()
    
    def get_messages_for_api(self) -> List[Dict[str, str]]:
        """Get messages in format suitable for API calls (without timestamps)"""
        return [
            {'role': msg['role'], 'content': msg['content']}
            for msg in self.history
        ]
    
    def clear(self) -> None:
        """Clear conversation history"""
        self.history.clear()
    
    def _trim_history(self) -> None:
        """Trim history to max_history length"""
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_last_n_messages(self, n: int) -> List[Dict[str, str]]:
        """Get last n messages"""
        return self.history[-n:] if n < len(self.history) else self.history
    
    def __len__(self) -> int:
        """Return number of messages in history"""
        return len(self.history)
