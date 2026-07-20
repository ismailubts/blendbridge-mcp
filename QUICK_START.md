# Quick Start Guide — blendbridge-mcp

Repository: [https://github.com/ismailubts/blendbridge-mcp](https://github.com/ismailubts/blendbridge-mcp)

## Install the Blender addon (directory layout)

The modular addon needs `core/`, `handlers/`, and `utils/` beside the addon entry files.

### Recommended layout

```
[Blender addons]/blendbridge_mcp/
├── __init__.py          ← from blendbridge_addon/__init__.py
├── addon_main.py        ← from blendbridge_addon/addon_main.py
├── core/
├── handlers/
└── utils/
```

Use `setup_blender_addon.sh` on macOS/Linux, or copy the files manually (see `INSTALLATION_DIRECTORY_SETUP.md`).

### Enable in Blender

1. Open Blender → **Edit > Preferences > Add-ons**
2. Search for **blendbridge-mcp**
3. Enable **Interface: blendbridge-mcp**
4. Restart Blender completely

### Start the bridge

1. In the 3D Viewport, press **N** for the sidebar
2. Open the **blendbridge-mcp** tab
3. Click **Start Bridge**
4. Confirm **Status: Live on port 9876** (or your configured port)

## Configure your MCP client

### Claude Desktop

Edit `claude_desktop_config.json` and add:

```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["blendbridge-mcp"]
    }
  }
}
```

### Cursor

In **Settings > MCP**, add the same `blender` server block.

Restart the client, then try: *Get information about the current Blender scene*.

## Troubleshooting

- **Server won't start**: change the port in the blendbridge-mcp panel; check the Blender console
- **MCP not connecting**: verify Blender shows a live port and `uvx blendbridge-mcp` works in a terminal
- **Few commands work**: ensure `core/`, `handlers/`, and `utils/` are installed next to `__init__.py`

See `README.md` for full documentation.
