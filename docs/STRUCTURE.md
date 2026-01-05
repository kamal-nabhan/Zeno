# Zeno Project Structure - Complete Overview

## 📁 Directory Tree

```
Zeno/
│
├── 📦 zeno/                          # Main Python package
│   ├── __init__.py                   # Package initialization
│   │
│   ├── 🎯 core/                      # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py                 # Configuration management (Config class)
│   │   ├── conversation.py           # Conversation history (ConversationManager)
│   │   └── speech.py                 # TTS & audio (SpeechManager)
│   │
│   ├── 🤖 ai/                        # AI backends
│   │   ├── __init__.py
│   │   ├── base.py                   # Abstract base class (BaseAI)
│   │   ├── local.py                  # Ollama backend (LocalAI)
│   │   └── openai.py                 # OpenAI Assistant (OpenAIAssistant)
│   │
│   ├── 🔌 integrations/              # External services
│   │   ├── __init__.py
│   │   ├── spotify.py                # Spotify control (SpotifyIntegration)
│   │   ├── weather.py                # Weather info (WeatherIntegration)
│   │   └── search.py                 # Image search (ImageSearch)
│   │
│   ├── ⚡ commands/                  # Command system
│   │   ├── __init__.py
│   │   ├── parser.py                 # Command parsing (CommandParser)
│   │   └── executor.py               # Command execution (CommandExecutor)
│   │
│   └── 🛠️ utils/                     # Utilities
│       ├── __init__.py
│       └── logger.py                 # Logging setup (setup_logger)
│
├── 🧪 tests/                         # Test suite
│   └── __init__.py
│
├── 📚 docs/                          # Documentation
│   ├── ARCHITECTURE.md               # Architecture details
│   ├── IMPROVEMENTS.md               # Future improvements
│   └── MIGRATION.md                  # Migration guide
│
├── 📜 scripts/                       # Utility scripts
│
├── 🚀 main.py                        # Entry point (NEW)
├── 🔧 config.py                      # Backward compatibility wrapper
├── 📋 requirements.txt               # Python dependencies
├── 🔐 .env.example                   # Environment template
├── 🔐 .env                           # Local configuration (gitignored)
├── 🚫 .gitignore                     # Git ignore rules
├── 📖 README.md                      # Project documentation
│
└── 🗂️ Old files (for reference):
    ├── assist.py                     # → zeno/ai/openai.py
    ├── assist_local.py               # → zeno/ai/local.py
    ├── spot.py                       # → zeno/integrations/spotify.py
    ├── tools.py                      # → zeno/commands/executor.py
    └── zeno.py                       # → main.py
```

## 🎯 Module Responsibilities

### Core Modules (`zeno/core/`)

| Module | Class/Function | Purpose |
|--------|---------------|---------|
| `config.py` | `Config` | Environment variables, validation, system prompt |
| `conversation.py` | `ConversationManager` | Track message history with timestamps |
| `speech.py` | `SpeechManager` | TTS generation and audio playback |

### AI Modules (`zeno/ai/`)

| Module | Class | Purpose |
|--------|-------|---------|
| `base.py` | `BaseAI` | Abstract interface for AI backends |
| `local.py` | `LocalAI` | Ollama-based local AI (default) |
| `openai.py` | `OpenAIAssistant` | OpenAI Assistant API backend |

### Integration Modules (`zeno/integrations/`)

| Module | Class | Purpose |
|--------|-------|---------|
| `spotify.py` | `SpotifyIntegration` | Music playback control |
| `weather.py` | `WeatherIntegration` | Weather information |
| `search.py` | `ImageSearch` | Google image search |

### Command Modules (`zeno/commands/`)

| Module | Class | Purpose |
|--------|-------|---------|
| `parser.py` | `CommandParser` | Extract commands from responses |
| `executor.py` | `CommandExecutor` | Execute parsed commands |

### Utility Modules (`zeno/utils/`)

| Module | Function | Purpose |
|--------|----------|---------|
| `logger.py` | `setup_logger()` | Configure logging |

## 🔄 Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                         User Speech                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Speech Recognition (RealtimeSTT)                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Hotword Detection                          │
│                   (Check for "zeno")                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI Backend (LocalAI)                      │
│              • Add to conversation history                   │
│              • Generate response with context                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Command Parser (CommandParser)                  │
│              • Split speech from commands                    │
│              • Detect questions                              │
└─────────────┬───────────────────────┬───────────────────────┘
              │                       │
              ▼                       ▼
┌──────────────────────┐   ┌──────────────────────────────────┐
│   Speech Text        │   │   Commands (if any)              │
└──────┬───────────────┘   └──────┬───────────────────────────┘
       │                          │
       ▼                          ▼
┌──────────────────────┐   ┌──────────────────────────────────┐
│  SpeechManager       │   │  CommandExecutor                 │
│  • Generate TTS      │   │  • Spotify control               │
│  • Play audio        │   │  • Weather info                  │
└──────────────────────┘   │  • Image search                  │
                           │  • Device control (placeholder)  │
                           └──────────────────────────────────┘
```

## 🔗 Import Dependencies

```
main.py
├── zeno.core.config (Config)
├── zeno.core.speech (SpeechManager)
├── zeno.ai.local (LocalAI)
├── zeno.commands.parser (CommandParser)
├── zeno.commands.executor (CommandExecutor)
└── zeno.utils.logger (setup_logger)

CommandExecutor
├── zeno.integrations.spotify (SpotifyIntegration)
├── zeno.integrations.weather (WeatherIntegration)
├── zeno.integrations.search (ImageSearch)
├── zeno.ai.base (BaseAI)
└── zeno.core.speech (SpeechManager)

LocalAI
├── zeno.core.config (config)
├── zeno.core.conversation (ConversationManager)
└── ollama (external)

All Integrations
└── zeno.core.config (config)
```

## 📊 File Statistics

| Category | Files | Lines of Code (est.) |
|----------|-------|---------------------|
| Core | 3 | ~300 |
| AI | 3 | ~200 |
| Integrations | 3 | ~250 |
| Commands | 2 | ~200 |
| Utils | 1 | ~50 |
| **Total Package** | **12** | **~1000** |
| Main Entry | 1 | ~100 |
| Tests | TBD | TBD |
| Docs | 3 | N/A |

## 🎨 Design Patterns Used

1. **Singleton Pattern**
   - `Config` class for global configuration

2. **Strategy Pattern**
   - `BaseAI` interface with multiple implementations

3. **Facade Pattern**
   - `CommandExecutor` simplifies complex integrations

4. **Dependency Injection**
   - Components receive dependencies in constructors

5. **Factory Pattern** (implicit)
   - Different AI backends created based on needs

## 🚀 Quick Start Commands

```bash
# 1. Setup environment
cp .env.example .env
# Edit .env with your credentials

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Ollama and pull model
ollama pull llama3.1

# 4. Run Zeno
python main.py

# 5. Check configuration
python -c "from zeno.core.config import config; config.print_status()"
```

## 📈 Scalability Features

✅ **Modular Design** - Easy to add new features
✅ **Clean Separation** - Each module has single responsibility
✅ **Type Hints** - Better IDE support and error catching
✅ **Error Handling** - Graceful degradation
✅ **Logging** - Built-in debugging support
✅ **Testing Ready** - Structure supports unit tests
✅ **Documentation** - Comprehensive docs in `/docs`
✅ **Backward Compatible** - Old imports still work

## 🎯 Next Steps

1. **Validate Setup**: Run `python main.py`
2. **Read Docs**: Check `docs/ARCHITECTURE.md`
3. **Plan Improvements**: See `docs/IMPROVEMENTS.md`
4. **Write Tests**: Add tests in `tests/`
5. **Extend Features**: Follow patterns in existing code

---

**The structure is now professional, scalable, and ready for growth!** 🚀
