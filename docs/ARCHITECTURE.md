# Zeno Architecture

## Directory Structure

```
Zeno/
├── zeno/                      # Main package
│   ├── __init__.py           # Package initialization
│   ├── core/                 # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py         # Configuration management
│   │   ├── conversation.py   # Conversation history
│   │   └── speech.py         # TTS and audio playback
│   ├── ai/                   # AI backends
│   │   ├── __init__.py
│   │   ├── base.py           # Base AI interface
│   │   ├── local.py          # Ollama backend
│   │   └── openai.py         # OpenAI Assistant backend
│   ├── integrations/         # External services
│   │   ├── __init__.py
│   │   ├── spotify.py        # Spotify control
│   │   ├── weather.py        # Weather info
│   │   └── search.py         # Image search
│   ├── commands/             # Command system
│   │   ├── __init__.py
│   │   ├── parser.py         # Command parsing
│   │   └── executor.py       # Command execution
│   └── utils/                # Utilities
│       ├── __init__.py
│       └── logger.py         # Logging setup
├── tests/                    # Test suite
│   └── __init__.py
├── docs/                     # Documentation
│   ├── IMPROVEMENTS.md       # Future improvements
│   └── ARCHITECTURE.md       # This file
├── scripts/                  # Utility scripts
├── main.py                   # Entry point
├── requirements.txt          # Dependencies
├── .env.example              # Environment template
├── .env                      # Local configuration
├── .gitignore               # Git ignore rules
└── README.md                 # Project documentation
```

## Component Overview

### Core Module (`zeno/core/`)

**Purpose**: Fundamental functionality that all other modules depend on.

- **`config.py`**: Centralized configuration management
  - Loads environment variables
  - Provides validation
  - Stores system prompt
  - Singleton pattern for global access

- **`conversation.py`**: Conversation history management
  - Tracks user and assistant messages
  - Maintains timestamps
  - Automatic history trimming
  - API-ready message formatting

- **`speech.py`**: Speech synthesis and playback
  - OpenAI TTS integration
  - Audio playback with pygame
  - Resource cleanup
  - Synchronous speech generation

### AI Module (`zeno/ai/`)

**Purpose**: AI backend implementations with a common interface.

- **`base.py`**: Abstract base class
  - Defines AI backend interface
  - Ensures consistent API across backends
  - Type hints for better IDE support

- **`local.py`**: Ollama implementation
  - Local LLM using Ollama
  - Conversation memory integration
  - Error handling
  - No API costs

- **`openai.py`**: OpenAI Assistant implementation
  - Cloud-based AI
  - Persistent threads
  - Advanced capabilities
  - Requires API key

### Integrations Module (`zeno/integrations/`)

**Purpose**: External service integrations.

- **`spotify.py`**: Music control
  - OAuth authentication
  - Playback control
  - Track information
  - Error handling

- **`weather.py`**: Weather information
  - Async weather API
  - Configurable city
  - Error handling

- **`search.py`**: Image search
  - Google image crawler
  - Directory management
  - Cleanup utilities

### Commands Module (`zeno/commands/`)

**Purpose**: Command parsing and execution system.

- **`parser.py`**: Command extraction
  - Parse hashtag commands from responses
  - Detect questions
  - Clean text extraction

- **`executor.py`**: Command execution
  - Delegates to appropriate integrations
  - Handles all command types
  - Error handling
  - Placeholder for future commands

### Utils Module (`zeno/utils/`)

**Purpose**: Shared utilities and helpers.

- **`logger.py`**: Logging configuration
  - Console and file logging
  - Configurable levels
  - Consistent formatting

## Data Flow

```
User Speech
    ↓
[Speech Recognition] (RealtimeSTT)
    ↓
[Hotword Detection]
    ↓
[AI Backend] (LocalAI or OpenAIAssistant)
    ↓
[Command Parser]
    ↓
├─→ [Speech Text] → [TTS] → [Audio Playback]
└─→ [Commands] → [Command Executor] → [Integrations]
```

## Design Patterns

### 1. **Singleton Pattern**
- `Config` class provides global configuration access
- Single instance shared across all modules

### 2. **Strategy Pattern**
- `BaseAI` defines interface
- Different AI backends implement the same interface
- Easy to swap backends

### 3. **Facade Pattern**
- `CommandExecutor` provides simple interface to complex integrations
- Hides integration details from main loop

### 4. **Dependency Injection**
- Components receive dependencies in constructor
- Easier testing and flexibility

## Module Dependencies

```
main.py
  ├── zeno.core.config
  ├── zeno.core.speech
  ├── zeno.ai.local
  ├── zeno.commands.parser
  ├── zeno.commands.executor
  └── zeno.utils.logger

zeno.commands.executor
  ├── zeno.integrations.spotify
  ├── zeno.integrations.weather
  ├── zeno.integrations.search
  ├── zeno.ai.base
  └── zeno.core.speech

zeno.ai.local
  ├── zeno.core.config
  └── zeno.core.conversation

zeno.integrations.*
  └── zeno.core.config
```

## Extension Points

### Adding a New Integration

1. Create new file in `zeno/integrations/`
2. Implement integration class
3. Add to `zeno/integrations/__init__.py`
4. Add commands to `CommandExecutor`
5. Update system prompt in `config.py`

### Adding a New AI Backend

1. Create new file in `zeno/ai/`
2. Inherit from `BaseAI`
3. Implement required methods
4. Add to `zeno/ai/__init__.py`
5. Update `main.py` to use new backend

### Adding a New Command Type

1. Add parsing logic to `CommandParser` (if needed)
2. Add execution logic to `CommandExecutor`
3. Update system prompt with new command format

## Testing Strategy

```
tests/
├── test_config.py           # Configuration tests
├── test_conversation.py     # Conversation management tests
├── test_commands.py         # Command parsing/execution tests
├── test_integrations.py     # Integration tests (with mocks)
└── test_ai.py              # AI backend tests (with mocks)
```

## Configuration Management

All configuration is centralized in `zeno/core/config.py`:

1. **Environment Variables**: Loaded from `.env` file
2. **Validation**: `Config.validate()` checks required settings
3. **Status**: `Config.print_status()` shows configuration state
4. **Type Safety**: Class attributes with type hints

## Error Handling Strategy

1. **Graceful Degradation**: Features fail independently
2. **User-Friendly Messages**: Clear error messages
3. **Logging**: All errors logged for debugging
4. **Fallbacks**: Default values for optional settings

## Future Improvements

See `docs/IMPROVEMENTS.md` for detailed improvement suggestions.

Key architectural improvements:
- Plugin system for dynamic feature loading
- Database for persistent conversation history
- Web API for remote control
- Event-driven architecture for better responsiveness
- Async/await throughout for better performance

---

**Last Updated**: 2026-01-05
