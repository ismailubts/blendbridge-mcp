# Cursor Setup Guide for BlendBridge

## Quick Setup for Cursor

### Step 1: Install Blender Addon

1. Run the setup script:
   ```bash
   cd blendbridge-mcp
   ./setup_blender_addon.sh
   ```

2. Or manually install (see [INSTALLATION_DIRECTORY_SETUP.md](INSTALLATION_DIRECTORY_SETUP.md))

3. Enable the addon in Blender

### Step 2: Configure Cursor MCP

**Option A: Global MCP Server (Recommended)**

1. Open Cursor
2. Go to **Settings** (Cmd+, on Mac)
3. Search for **"MCP"** or go to **MCP** section
4. Click **"Add Server"** or **"Add new global MCP server"**
5. Paste this configuration:

```json
{
    "mcpServers": {
        "blender": {
            "command": "uvx",
            "args": [
                "blendbridge-mcp"
            ]
        },
        "filesystem": {
            "command": "npx",
            "args": [
              "-y",
              "@modelcontextprotocol/server-filesystem",
              "/path/to/your/Desktop",
              "/path/to/your/Downloads"
            ]
        }
    }
}
```

**Option B: Project-Specific MCP Server**

1. In your project root, create `.cursor/mcp.json`
2. Add the same configuration as above

### Step 3: Restart Cursor

1. **Completely quit Cursor** (Cmd+Q on Mac)
2. **Reopen Cursor**
3. You should see BlendBridge tools available

### Step 4: Verify Connection

1. **Start Blender** and enable the addon
2. **Start the MCP server** in Blender (BlendBridge panel)
3. In Cursor, you should see BlendBridge tools available

## Using BlendBridge in Cursor

Once configured, you can use commands like:

- "Get information about the current Blender scene"
- "Create a keyframe for the cube object"
- "Set render output to /tmp/renders/"
- "Search for chair models on Sketchfab"

Cursor will automatically use the BlendBridge tools when you mention Blender-related tasks.

## Troubleshooting

### "BlendBridge not showing in Cursor"
- Make sure you restarted Cursor completely
- Check Cursor's MCP settings to see if blender server is listed
- Verify `uvx blendbridge-mcp` works in terminal: `uvx blendbridge-mcp --help`

### "Connection to Blender failed"
- Make sure Blender is running
- Check that the addon is enabled in Blender
- Verify the server is started (check BlendBridge panel)
- Check Blender console for errors

### "MCP config errors"
- Validate your JSON at jsonlint.com
- Make sure there's a comma between server entries
- Check that all quotes are properly escaped

## Configuration Examples

### Blender Only
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

### Blender + Filesystem
```json
{
    "mcpServers": {
        "blender": {
            "command": "uvx",
            "args": ["blendbridge-mcp"]
        },
        "filesystem": {
            "command": "npx",
            "args": [
              "-y",
              "@modelcontextprotocol/server-filesystem",
              "/path/to/your/Desktop",
              "/path/to/your/Downloads"
            ]
        }
    }
}
```

### Multiple Servers
You can add as many MCP servers as you need:
```json
{
    "mcpServers": {
        "blender": {
            "command": "uvx",
            "args": ["blendbridge-mcp"]
        },
        "filesystem": {
            "command": "npx",
            "args": [
              "-y",
              "@modelcontextprotocol/server-filesystem",
              "/path/to/dir1",
              "/path/to/dir2"
            ]
        },
        "another-server": {
            "command": "npx",
            "args": ["-y", "@some/other-server"]
        }
    }
}
```

## Quick Test

After setup, try asking Cursor:
- "What objects are in the current Blender scene?"
- "Create a cube in Blender at position (0, 0, 0)"
- "Get the current frame number in Blender"

If it works, you'll see Cursor using the BlendBridge tools!
