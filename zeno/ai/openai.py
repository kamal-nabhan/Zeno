"""
OpenAI Assistant backend
"""
from openai import OpenAI
import time
from zeno.ai.base import BaseAI
from zeno.core.config import config


class OpenAIAssistant(BaseAI):
    """OpenAI Assistant API backend"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=config.OPENAI_API_KEY,
            default_headers={"OpenAI-Beta": "assistants=v2"}
        )
        
        self.assistant_id = config.OPENAI_ASSISTANT_ID
        self.thread_id = config.OPENAI_THREAD_ID
        
        # Validate configuration
        if not self.assistant_id or not self.thread_id:
            raise ValueError(
                "OpenAI Assistant requires OPENAI_ASSISTANT_ID and OPENAI_THREAD_ID "
                "to be set in .env file"
            )
        
        # Retrieve assistant and thread
        try:
            self.assistant = self.client.beta.assistants.retrieve(self.assistant_id)
            self.thread = self.client.beta.threads.retrieve(self.thread_id)
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenAI Assistant: {str(e)}")
    
    def ask(self, question: str) -> str:
        """
        Ask a question using OpenAI Assistant
        
        Args:
            question: The user's question
            
        Returns:
            The AI's response
        """
        try:
            # Add message to thread
            self.client.beta.threads.messages.create(
                self.thread.id,
                role="user",
                content=question
            )
            
            # Create and wait for run to complete
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id
            )
            
            # Poll for completion
            while True:
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id,
                    run_id=run.id
                )
                
                if run_status.status == 'completed':
                    break
                elif run_status.status == 'failed':
                    return "I apologize, Sir. The request failed."
                
                time.sleep(1)
            
            # Get the latest message
            messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
            return messages.data[0].content[0].text.value
            
        except Exception as e:
            error_msg = f"OpenAI Assistant error: {str(e)}"
            print(error_msg)
            return "I apologize, Sir. I encountered a technical difficulty."
    
    def reset_conversation(self) -> None:
        """
        Reset conversation by creating a new thread
        Note: This creates a new thread, old thread is not deleted
        """
        try:
            self.thread = self.client.beta.threads.create()
            self.thread_id = self.thread.id
            print(f"New thread created: {self.thread_id}")
            print("Update OPENAI_THREAD_ID in .env to persist this thread")
        except Exception as e:
            print(f"Failed to create new thread: {str(e)}")
    
    @property
    def name(self) -> str:
        """Return the name of this AI backend"""
        return f"OpenAI Assistant ({self.assistant_id[:8]}...)"
