# Setup Instructions — Modular blendbridge-mcp Addon

Repository: [https://github.com/ismailubts/blendbridge-mcp](https://github.com/ismailubts/blendbridge-mcp)

## Required directory structure

```
[Blender addons folder]/blendbridge_mcp/
├── __init__.py          ← blendbridge_addon/__init__.py
├── addon_main.py        ← blendbridge_addon/addon_main.py
├── core/
├── handlers/
└── utils/
```

## Quick setup

### Option 1: Setup script (macOS/Linux)

```bash
./setup_blender_addon.sh
```

### Option 2: Manual copy

```bash
mkdir -p "[Blender addons]/blendbridge_mcp"
cp blendbridge_addon/__init__.py "[Blender addons]/blendbridge_mcp/__init__.py"
cp blendbridge_addon/addon_main.py "[Blender addons]/blendbridge_mcp/addon_main.py"
cp -r core handlers utils "[Blender addons]/blendbridge_mcp/"
```

## Verification

After restarting Blender, the console should show handler registration and:

```
blendbridge-mcp addon registered (v2.0)
```

If you only see a fallback server with two commands, the `core/`, `handlers/`, and `utils/` folders are missing or not on the Python path.

## Testing

```bash
python test_mcp_actions.py
```

Most commands should pass when the modular system is loaded.

See `INSTALLATION_DIRECTORY_SETUP.md` for platform-specific paths.
