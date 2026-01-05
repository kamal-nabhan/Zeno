"""
Base AI interface for Zeno
All AI backends should inherit from this
"""
from abc import ABC, abstractmethod
from typing import Optional


class BaseAI(ABC):
    """Abstract base class for AI backends"""
    
    @abstractmethod
    def ask(self, question: str) -> str:
        """
        Ask a question and get a response
        
        Args:
            question: The user's question
            
        Returns:
            The AI's response
        """
        pass
    
    @abstractmethod
    def reset_conversation(self) -> None:
        """Reset the conversation history"""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this AI backend"""
        pass
