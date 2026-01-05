"""
Zeno - Stoic AI Assistant
Main entry point for the voice-activated assistant
"""
from RealtimeSTT import AudioToTextRecorder
import time
from zeno.core.config import config
from zeno.core.speech import SpeechManager
from zeno.ai.local import LocalAI
from zeno.commands.parser import CommandParser
from zeno.commands.executor import CommandExecutor
from zeno.utils.logger import setup_logger


def main():
    """Main entry point for Zeno"""
    
    # Setup logger
    logger = setup_logger()
    
    # Print configuration status
    config.print_status()
    
    # Validate configuration
    is_valid, warnings = config.validate()
    if not is_valid:
        logger.error("Configuration is invalid. Please check your .env file.")
        return
    
    # Initialize components
    logger.info("Initializing Zeno...")
    
    try:
        # Initialize AI backend
        ai = LocalAI()
        logger.info(f"AI Backend: {ai.name}")
        
        # Initialize speech manager
        speech = SpeechManager()
        logger.info("Speech manager initialized")
        
        # Initialize command system
        parser = CommandParser()
        executor = CommandExecutor(ai, speech)
        logger.info("Command system initialized")
        
        # Initialize speech recognition
        recorder = AudioToTextRecorder(
            spinner=False,
            model=config.WHISPER_MODEL,
            language="en",
            post_speech_silence_duration=config.POST_SPEECH_SILENCE,
            silero_sensitivity=config.SILERO_SENSITIVITY
        )
        logger.info("Speech recognition initialized")
        
    except Exception as e:
        logger.error(f"Failed to initialize: {str(e)}")
        return
    
    # Main loop
    hotwords = [config.HOTWORD.lower()]
    skip_hotword_check = False
    
    print("\n" + "=" * 50)
    print(f"Zeno is listening... Say '{config.HOTWORD}' to activate.")
    print("=" * 50 + "\n")
    
    try:
        while True:
            current_text = recorder.text()
            
            if not current_text:
                continue
            
            # Check for hotword or if we should skip the check
            if any(hotword in current_text.lower() for hotword in hotwords) or skip_hotword_check:
                logger.info(f"User: {current_text}")
                recorder.stop()
                
                # Append timestamp to the query
                timestamped_text = current_text + " " + time.strftime("%Y-%m-%d %H:%M:%S")
                
                # Get response from AI
                response = ai.ask(timestamped_text)
                logger.info(f"Zeno: {response}")
                
                # Parse response
                speech_text, commands = parser.parse(response)
                
                # Speak the response
                speech.speak(speech_text)
                
                # Execute any commands
                if commands:
                    logger.info(f"Executing commands: {commands}")
                    executor.execute(commands)
                
                # Check if we should continue listening (question asked)
                skip_hotword_check = parser.has_question(response)
                
                recorder.start()
    
    except KeyboardInterrupt:
        logger.info("\nShutting down Zeno...")
        speech.cleanup()
        logger.info("Goodbye, Sir.")
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        speech.cleanup()


if __name__ == '__main__':
    main()
