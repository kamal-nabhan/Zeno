"""
Zeno - Stoic AI Assistant

A voice-activated AI assistant with Stoic philosophy,
featuring real-time speech recognition and intelligent conversation.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from zeno.core.config import Config
from zeno.ai.local import LocalAI
from zeno.ai.openai import OpenAIAssistant

__all__ = ['Config', 'LocalAI', 'OpenAIAssistant']
