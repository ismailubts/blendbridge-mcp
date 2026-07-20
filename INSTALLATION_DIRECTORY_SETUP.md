# How to Install blendbridge-mcp as a Directory Addon

Repository: [https://github.com/ismailubts/blendbridge-mcp](https://github.com/ismailubts/blendbridge-mcp)

## Why directory install?

Installing only a single Python file prevents Blender from loading `core/`, `handlers/`, and `utils/`. You will miss render and Sketchfab handlers and get a reduced command set.

## Install steps

### 1. Create the addon directory

**macOS:**

```bash
cd ~/Library/Application\ Support/Blender/[version]/scripts/addons/
mkdir -p blendbridge_mcp
```

Replace `[version]` with your Blender version (for example `4.2`).

**Windows:**

```powershell
mkdir "$env:APPDATA\Blender Foundation\Blender\[version]\scripts\addons\blendbridge_mcp"
```

### 2. Copy files from this repository

From the cloned `blendbridge-mcp` directory:

```bash
cp blendbridge_addon/__init__.py ~/Library/Application\ Support/Blender/[version]/scripts/addons/blendbridge_mcp/__init__.py
cp blendbridge_addon/addon_main.py ~/Library/Application\ Support/Blender/[version]/scripts/addons/blendbridge_mcp/addon_main.py
cp -r core handlers utils ~/Library/Application\ Support/Blender/[version]/scripts/addons/blendbridge_mcp/
```

Or run `./setup_blender_addon.sh` on macOS/Linux.

### 3. Expected layout

```
blendbridge_mcp/
├── __init__.py
├── addon_main.py
├── core/
├── handlers/
└── utils/
```

### 4. Enable in Blender

1. **Edit > Preferences > Add-ons**
2. Search for **blendbridge-mcp**
3. Enable **Interface: blendbridge-mcp**
4. Restart Blender completely

### 5. Verify

The Blender console should report handler registration (28+ handlers when render and Sketchfab modules load).

## Symbolic link (development)

```bash
mkdir -p ~/Library/Application\ Support/Blender/[version]/scripts/addons/blendbridge_mcp
ln -s /path/to/blendbridge-mcp/blendbridge_addon/__init__.py ~/Library/Application\ Support/Blender/[version]/scripts/addons/blendbridge_mcp/__init__.py
ln -s /path/to/blendbridge-mcp/blendbridge_addon/addon_main.py ~/Library/Application\ Support/Blender/[version]/scripts/addons/blendbridge_mcp/addon_main.py
ln -s /path/to/blendbridge-mcp/core ~/Library/Application\ Support/Blender/[version]/scripts/addons/blendbridge_mcp/core
ln -s /path/to/blendbridge-mcp/handlers ~/Library/Application\ Support/Blender/[version]/scripts/addons/blendbridge_mcp/handlers
ln -s /path/to/blendbridge-mcp/utils ~/Library/Application\ Support/Blender/[version]/scripts/addons/blendbridge_mcp/utils
```

Replace `/path/to/blendbridge-mcp` with your local clone path.
