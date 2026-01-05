# Old Structure Archive

This folder contains the original flat file structure before the reorganization.

## Files Archived

These files have been replaced by the new modular structure:

| Old File | New Location |
|----------|-------------|
| `assist.py` | `zeno/ai/openai.py` |
| `assist_local.py` | `zeno/ai/local.py` |
| `spot.py` | `zeno/integrations/spotify.py` |
| `tools.py` | `zeno/commands/executor.py` |
| `zeno.py` | `main.py` |

## Why Archived?

These files are kept for reference during the transition period. They can be safely deleted once you've verified the new structure works correctly.

## Migration

See `../docs/MIGRATION.md` for details on how the code was reorganized.

## When to Delete

You can delete this entire folder once:
1. ✅ You've tested the new `main.py` successfully
2. ✅ All integrations work as expected
3. ✅ You're comfortable with the new structure
4. ✅ You've updated any custom code to use new imports

## Deleting This Folder

```bash
# Windows PowerShell
Remove-Item -Recurse -Force old_structure

# Or just delete it in File Explorer
```

---

**Note**: The root `config.py` is NOT in this folder - it's a backward compatibility wrapper and should be kept in the root directory.
