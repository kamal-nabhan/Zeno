"""
Local AI backend using Ollama
"""
import ollama
from zeno.ai.base import BaseAI
from zeno.core.config import config
from zeno.core.conversation import ConversationManager


class LocalAI(BaseAI):
    """Local AI backend using Ollama"""
    
    def __init__(self):
        self.conversation = ConversationManager()
        self.model = config.OLLAMA_MODEL
        self.system_prompt = config.SYSTEM_PROMPT
    
    def ask(self, question: str) -> str:
        """
        Ask a question using Ollama
        
        Args:
            question: The user's question
            
        Returns:
            The AI's response
        """
        try:
            # Add user message to history
            self.conversation.add_user_message(question)
            
            # Prepare messages for API
            messages = [
                {'role': 'system', 'content': self.system_prompt},
                *self.conversation.get_messages_for_api()
            ]
            
            # Get response from Ollama
            response = ollama.chat(model=self.model, messages=messages)
            
            # Extract response content
            response_text = response['message']['content']
            
            # Add assistant response to history
            self.conversation.add_assistant_message(response_text)
            
            return response_text
            
        except ollama.ResponseError as e:
            error_msg = f"Ollama error: {str(e)}"
            print(error_msg)
            return "I apologize, Sir. I encountered a technical difficulty."
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(error_msg)
            return "I apologize, Sir. An unexpected error occurred."
    
    def reset_conversation(self) -> None:
        """Reset the conversation history"""
        self.conversation.clear()
    
    @property
    def name(self) -> str:
        """Return the name of this AI backend"""
        return f"Ollama ({self.model})"
