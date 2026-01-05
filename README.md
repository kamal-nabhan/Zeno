# Zeno - Stoic AI Assistant

A voice-activated AI assistant inspired by Stoic philosophy, featuring real-time speech recognition, intelligent conversation with memory, and text-to-speech responses. Zeno can control Spotify, provide weather information, search for images, and more.

## Features

- **Real-Time Speech Recognition**: Leveraging Whisper for accurate speech-to-text conversion
- **Intelligent Response Generation**: Uses Ollama (llama3.1) locally or OpenAI's GPT models for context-aware responses
- **Stoic Personality**: Formal, disciplined, and philosophical AI assistant
- **Speech Output**: Converts text responses to speech using OpenAI's TTS
- **Hotword Detection**: Activates on the word "Zeno"
- **Conversation Memory**: Maintains context across multiple interactions
- **Spotify Integration**: Control playback, skip tracks, get current song info
- **Weather Information**: Get weather updates for your configured city
- **Image Search**: Download images using Google Image Crawler
- **Extensible Command System**: Easy to add new integrations
- **Modular Architecture**: Clean, organized codebase following best practices

## Requirements

- Python 3.9+
- OpenAI API key (for TTS and optional GPT assistant)
- Ollama installed locally (for local LLM)
- Spotify Developer credentials (optional, for music control)

## Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd Zeno
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Ollama** (for local AI)
   - Visit [ollama.ai](https://ollama.ai) and install Ollama
   - Pull the llama3.1 model:
   ```bash
   ollama pull llama3.1
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Fill in your API keys and credentials:
   ```bash
   cp .env.example .env
   ```
   
   Required:
   - `OPENAI_API_KEY`: Your OpenAI API key (for TTS)
   
   Optional:
   - `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `SPOTIFY_USERNAME`: For Spotify control
   - `OPENAI_ASSISTANT_ID`, `OPENAI_THREAD_ID`: If using OpenAI Assistants API instead of Ollama
   - `NOTION_API_KEY`, `NOTION_DATABASE_ID`: For future Notion integration

## Configuration

Edit the `.env` file to customize:

- `DEFAULT_CITY`: City for weather information (default: Chicago)
- `TTS_VOICE`: OpenAI TTS voice (default: echo)
- `TTS_MODEL`: OpenAI TTS model (default: tts-1)
- `OLLAMA_MODEL`: Ollama model to use (default: llama3.1)
- `HOTWORD`: Wake word to activate Zeno (default: zeno)
- `WHISPER_MODEL`: Speech recognition model (default: tiny.en)

## Usage

### Running Zeno

```bash
python main.py
```

### Interacting with Zeno

1. Wait for "Zeno is listening..." message
2. Say "Zeno" followed by your command
3. Examples:
   - "Zeno, what's the weather like?"
   - "Zeno, play some music"
   - "Zeno, what song is playing?"
   - "Zeno, skip this track"
   - "Zeno, pause the music"

### Available Commands

Zeno automatically detects and executes commands embedded in responses:

- **Spotify**: `#spotify-play`, `#spotify-pause`, `#spotify-skip`, `#spotify-previous`, `#spotify-info`
- **Weather**: Automatically triggered when asking about weather
- **Search**: `#search-<query>` - Downloads images
- **Device Control** (placeholders): `#lights-1/0`, `#3d_printer-1/0`

## Project Structure

```
Zeno/
├── zeno/                      # Main package
│   ├── core/                  # Core functionality
│   │   ├── config.py          # Configuration management
│   │   ├── conversation.py    # Conversation history
│   │   └── speech.py          # TTS and audio
│   ├── ai/                    # AI backends
│   │   ├── base.py            # Base interface
│   │   ├── local.py           # Ollama backend
│   │   └── openai.py          # OpenAI backend
│   ├── integrations/          # External services
│   │   ├── spotify.py         # Spotify control
│   │   ├── weather.py         # Weather info
│   │   └── search.py          # Image search
│   ├── commands/              # Command system
│   │   ├── parser.py          # Command parsing
│   │   └── executor.py        # Command execution
│   └── utils/                 # Utilities
│       └── logger.py          # Logging
├── tests/                     # Test suite
├── docs/                      # Documentation
│   ├── ARCHITECTURE.md        # Architecture details
│   └── IMPROVEMENTS.md        # Future improvements
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

For detailed architecture information, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Switching Between Local and Cloud AI

By default, Zeno uses **Ollama** for local AI processing. To use OpenAI's Assistants API instead:

1. Set up an assistant at [platform.openai.com/assistants](https://platform.openai.com/assistants)
2. Add `OPENAI_ASSISTANT_ID` and `OPENAI_THREAD_ID` to your `.env`
3. In `main.py`, change:
   ```python
   from zeno.ai.local import LocalAI
   ai = LocalAI()
   
   # Change to:
   from zeno.ai.openai import OpenAIAssistant
   ai = OpenAIAssistant()
   ```

## Customizing Zeno's Personality

Edit the `SYSTEM_PROMPT` in `zeno/core/config.py` to change Zeno's personality, constraints, or capabilities.

## Extending Functionality

### Adding New Commands

1. Add command logic to `zeno/commands/executor.py`
2. Update the `SYSTEM_PROMPT` in `zeno/core/config.py`
3. Zeno will automatically use the new commands

### Adding New Integrations

1. Create a new module in `zeno/integrations/`
2. Import it in `zeno/commands/executor.py`
3. Add command parsing logic
4. Update system prompt with new capabilities

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed extension guidelines.

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Style

This project follows PEP 8 guidelines. Use type hints where appropriate.

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Troubleshooting

**Microphone not detected:**
- Ensure your microphone is set as the default recording device
- Check PyAudio installation

**Ollama errors:**
- Verify Ollama is running: `ollama list`
- Ensure llama3.1 model is pulled: `ollama pull llama3.1`

**Spotify not working:**
- Verify credentials in `.env`
- Ensure Spotify is running and you're logged in
- Check redirect URI matches in Spotify Developer Dashboard

**TTS not working:**
- Verify `OPENAI_API_KEY` is set correctly
- Check your OpenAI account has API credits

**Import errors:**
- Ensure you're running from the project root directory
- Try: `python -m pip install -e .` to install in development mode

## Future Improvements

See [docs/IMPROVEMENTS.md](docs/IMPROVEMENTS.md) for a comprehensive list of planned enhancements, including:

- Plugin system for dynamic feature loading
- Database for conversation history
- Web dashboard
- Home Assistant integration
- RAG for personal documents
- And much more!

## License

Distributed under the MIT License. See LICENSE for more information.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or support, please open an issue on GitHub.

---

**"Virtue lies in action, Sir."** - Zeno
