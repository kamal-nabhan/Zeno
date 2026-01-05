# Migration Guide

## Migrating from Old Structure to New Structure

This guide helps you transition from the old flat file structure to the new organized package structure.

## What Changed?

### Old Structure
```
Zeno/
├── zeno.py
├── assist.py
├── assist_local.py
├── spot.py
├── tools.py
├── config.py
└── requirements.txt
```

### New Structure
```
Zeno/
├── zeno/                    # Package directory
│   ├── core/               # Core functionality
│   ├── ai/                 # AI backends
│   ├── integrations/       # External services
│   ├── commands/           # Command system
│   └── utils/              # Utilities
├── main.py                 # New entry point
├── config.py               # Backward compatibility wrapper
└── requirements.txt
```

## Breaking Changes

### 1. Entry Point Changed

**Old:**
```bash
python zeno.py
```

**New:**
```bash
python main.py
```

### 2. Import Paths Changed

**Old:**
```python
import config
import assist_local
from tools import parse_command
```

**New:**
```python
from zeno.core.config import config
from zeno.ai.local import LocalAI
from zeno.commands.executor import CommandExecutor
```

### 3. Module Names Changed

| Old File | New Location |
|----------|-------------|
| `config.py` | `zeno/core/config.py` |
| `assist_local.py` | `zeno/ai/local.py` |
| `assist.py` | `zeno/ai/openai.py` |
| `spot.py` | `zeno/integrations/spotify.py` |
| `tools.py` | `zeno/commands/executor.py` |
| `zeno.py` | `main.py` |

## Migration Steps

### Step 1: Update Your Code

If you have custom code that imports the old modules:

**Before:**
```python
import config
import assist_local as assist

response = assist.ask_question_memory("Hello")
assist.TTS(response)
```

**After:**
```python
from zeno.core.config import config
from zeno.ai.local import LocalAI
from zeno.core.speech import SpeechManager

ai = LocalAI()
speech = SpeechManager()

response = ai.ask("Hello")
speech.speak(response)
```

### Step 2: Update Configuration

The configuration is now class-based:

**Before:**
```python
import config
print(config.OPENAI_API_KEY)
```

**After:**
```python
from zeno.core.config import config
print(config.OPENAI_API_KEY)
```

Note: The root `config.py` still works for backward compatibility!

### Step 3: Update Command Execution

**Before:**
```python
from tools import parse_command
parse_command("spotify-play")
```

**After:**
```python
from zeno.commands.executor import CommandExecutor
from zeno.ai.local import LocalAI
from zeno.core.speech import SpeechManager

ai = LocalAI()
speech = SpeechManager()
executor = CommandExecutor(ai, speech)
executor.execute(["spotify-play"])
```

## Backward Compatibility

### Old Files Still Work

The root `config.py` is a compatibility wrapper. Old code like this still works:

```python
import config
print(config.OPENAI_API_KEY)  # Still works!
```

### Gradual Migration

You can migrate gradually:

1. Start using `main.py` instead of `zeno.py`
2. Keep using old imports temporarily
3. Migrate imports one module at a time
4. Test after each change

## New Features in Refactored Code

### 1. Better Error Handling

All modules now have comprehensive error handling:

```python
from zeno.ai.local import LocalAI

ai = LocalAI()
response = ai.ask("Hello")  # Handles errors gracefully
```

### 2. Logging Support

```python
from zeno.utils.logger import setup_logger

logger = setup_logger()
logger.info("Starting Zeno")
```

### 3. Configuration Validation

```python
from zeno.core.config import config

is_valid, warnings = config.validate()
if not is_valid:
    print("Configuration invalid!")

config.print_status()  # Show configuration status
```

### 4. Conversation Management

```python
from zeno.core.conversation import ConversationManager

conv = ConversationManager()
conv.add_user_message("Hello")
conv.add_assistant_message("Hi there!")
print(len(conv))  # Number of messages
```

### 5. Cleaner Speech Management

```python
from zeno.core.speech import SpeechManager

speech = SpeechManager()
speech.speak("Hello, Sir")  # Generates TTS and plays
```

## API Changes

### AI Backends

**Old API:**
```python
import assist_local as assist

response = assist.ask_question_memory("Hello")
```

**New API:**
```python
from zeno.ai.local import LocalAI

ai = LocalAI()
response = ai.ask("Hello")
ai.reset_conversation()  # Clear history
print(ai.name)  # "Ollama (llama3.1)"
```

### Spotify Integration

**Old API:**
```python
import spot

spot.start_music()
info = spot.get_current_playing_info()
```

**New API:**
```python
from zeno.integrations.spotify import SpotifyIntegration

spotify = SpotifyIntegration()
if spotify.is_available():
    spotify.play()
    info = spotify.get_current_track()
```

### Weather Integration

**Old API:**
```python
from tools import get_weather
import asyncio

weather = asyncio.run(get_weather("Chicago"))
```

**New API:**
```python
from zeno.integrations.weather import WeatherIntegration

weather = WeatherIntegration()
info = weather.get_weather("Chicago")  # Handles async internally
```

## Testing Your Migration

1. **Run the new main.py:**
   ```bash
   python main.py
   ```

2. **Check configuration:**
   ```python
   from zeno.core.config import config
   config.print_status()
   ```

3. **Test each integration:**
   ```python
   from zeno.integrations.spotify import SpotifyIntegration
   spotify = SpotifyIntegration()
   print(spotify.is_available())
   ```

## Troubleshooting

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'zeno'`

**Solution:** Make sure you're running from the project root:
```bash
cd /path/to/Zeno
python main.py
```

Or install in development mode:
```bash
pip install -e .
```

### Old Files Interfering

If you have issues, you can safely delete the old files:

```bash
# These are no longer needed (backed up in git)
rm assist.py
rm assist_local.py
rm spot.py
rm tools.py
rm zeno.py
```

**Keep:** `config.py` (backward compatibility wrapper)

### Configuration Not Loading

Make sure `.env` file is in the project root, not in the `zeno/` directory.

## Benefits of New Structure

1. **Better Organization**: Related code is grouped together
2. **Easier Testing**: Each module can be tested independently
3. **Clearer Dependencies**: Import paths show relationships
4. **Scalability**: Easy to add new features
5. **Professional**: Follows Python best practices
6. **Type Safety**: Better IDE support with type hints
7. **Error Handling**: Comprehensive error handling throughout
8. **Logging**: Built-in logging support

## Need Help?

- Check [docs/ARCHITECTURE.md](ARCHITECTURE.md) for detailed structure
- See [docs/IMPROVEMENTS.md](IMPROVEMENTS.md) for future plans
- Open an issue on GitHub

---

**The old structure still works, but we recommend migrating to the new structure for better maintainability!**
