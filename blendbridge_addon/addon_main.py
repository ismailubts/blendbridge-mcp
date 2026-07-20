# blendbridge-mcp © 2026
# Enhanced with comprehensive blendbridge-mcp system

import bpy
from bpy.props import IntProperty, BoolProperty
import os
import sys

# Add current directory to path for imports
# Blender addons can be installed as single files or directories
blendbridge_mcp_dir = os.path.dirname(os.path.abspath(__file__))
if blendbridge_mcp_dir not in sys.path:
    sys.path.insert(0, blendbridge_mcp_dir)

# Try to import new modular system
# If modules don't exist, we'll handle gracefully
try:
    from core.server import BlendBridgeServer
    from handlers.handler_registry import register_all_handlers
    from utils.logger import logger
    MODULAR_SYSTEM_AVAILABLE = True
except ImportError as e:
    # If modular system not available, use fallback
    print(f"Warning: Modular system not available: {e}")
    print(f"Addon directory: {blendbridge_mcp_dir}")
    print(f"Python path: {sys.path[:3]}")
    MODULAR_SYSTEM_AVAILABLE = False
    # Create minimal fallback
    class BlendBridgeServer:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("Modular system not available. Please install as directory addon.")
    
    def register_all_handlers():
        pass
    
    class logger:
        @staticmethod
        def info(msg):
            print(f"INFO: {msg}")
        @staticmethod
        def error(msg):
            print(f"ERROR: {msg}")
        @staticmethod
        def warning(msg):
            print(f"WARNING: {msg}")

# Import existing integration code (will be preserved)
# This will be handled by creating wrapper handlers

bl_info = {
    "name": "blendbridge-mcp",
    "author": "ismailubts",
    "version": (2, 0, 0),  # Updated version
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > blendbridge-mcp",
    "description": "Connect Blender to Claude via MCP - Comprehensive Edition",
    "category": "Interface",
}

RODIN_FREE_TRIAL_KEY = "k9TcfFoEhNd9cCPP2guHAHHHkctZHIRhZDywZ1euGUXwihbYLpOjQhofby80NJez"

# Import existing integration handlers
# These will be created as wrapper handlers that use the original methods
# For now, we'll import the original addon methods

# Load original addon methods for integrations
# We'll create a compatibility layer

class IntegrationCompatibility:
    """Compatibility layer for existing integrations"""
    
    @staticmethod
    def load_original_methods():
        """Load methods from original addon.py"""
        # This will be populated with original integration methods
        # For now, we'll create stub handlers
        pass

# Register all new handlers (only if modular system is available)
if MODULAR_SYSTEM_AVAILABLE:
    try:
        register_all_handlers()
        logger.info("All handlers registered successfully")
    except Exception as e:
        logger.error(f"Error registering handlers: {e}")
        import traceback
        traceback.print_exc()
else:
    print("Modular system not available - handlers will not be registered")

# Blender Addon Preferences (preserved from original)
class BLENDBRIDGE_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    telemetry_consent: BoolProperty(
        name="Allow Anonymized Prompt Collection",
        description="Allow collection of anonymized prompts to help improve blendbridge-mcp",
        default=True
    )

    def draw(self, context):
        layout = self.layout
        
        # Telemetry section
        layout.label(text="Telemetry & Privacy:", icon='PREFERENCES')
        
        box = layout.box()
        row = box.row()
        row.prop(self, "telemetry_consent", text="Allow Anonymized Prompt Collection")
        
        # Info text
        box.separator()
        box.label(text="All data is anonymized and helps improve blendbridge-mcp.", icon='INFO')
        box.label(text="You can opt out anytime by unchecking the box above.", icon='INFO')
        
        # Terms and Conditions link
        box.separator()
        row = box.row()
        row.operator("blendbridge.open_terms", text="View Terms and Conditions", icon='TEXT')

# blendbridge-mcp sidebar panel
class BLENDBRIDGE_PT_Panel(bpy.types.Panel):
    bl_label = "blendbridge-mcp"
    bl_idname = "BLENDBRIDGE_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'blendbridge-mcp'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Brand header
        header = layout.box()
        header.label(text="blendbridge-mcp", icon='LINKED')
        header.label(text="MCP bridge for Blender")

        # Connection
        conn = layout.box()
        conn.label(text="Connection", icon='NETWORK_DRIVE')
        conn.prop(scene, "blendbridge_port", text="Port")
        if not scene.blendbridge_server_running:
            row = conn.row(align=True)
            row.scale_y = 1.3
            row.operator("blendbridge.start_server", text="Start Bridge", icon='PLAY')
            conn.label(text="Status: Offline", icon='RADIOBUT_OFF')
        else:
            row = conn.row(align=True)
            row.scale_y = 1.3
            row.operator("blendbridge.stop_server", text="Stop Bridge", icon='PAUSE')
            conn.label(text=f"Status: Live on {scene.blendbridge_port}", icon='RADIOBUT_ON')

        # Asset integrations
        assets = layout.box()
        assets.label(text="Asset Sources", icon='ASSET_MANAGER')
        assets.prop(scene, "blendbridge_use_polyhaven", text="Poly Haven")

        assets.prop(scene, "blendbridge_use_sketchfab", text="Sketchfab")
        if scene.blendbridge_use_sketchfab:
            sub = assets.box()
            sub.prop(scene, "blendbridge_sketchfab_api_key", text="API Key")

        # Generative models
        gen = layout.box()
        gen.label(text="3D Generation", icon='MESH_MONKEY')
        gen.prop(scene, "blendbridge_use_hyper3d", text="Hyper3D Rodin")
        if scene.blendbridge_use_hyper3d:
            sub = gen.box()
            sub.prop(scene, "blendbridge_hyper3d_mode", text="Mode")
            sub.prop(scene, "blendbridge_hyper3d_api_key", text="API Key")
            sub.operator("blendbridge.set_hyper3d_free_trial_api_key", text="Use Free Trial Key")

        gen.prop(scene, "blendbridge_use_hunyuan3d", text="Hunyuan3D")
        if scene.blendbridge_use_hunyuan3d:
            sub = gen.box()
            sub.prop(scene, "blendbridge_hunyuan3d_mode", text="Mode")
            if scene.blendbridge_hunyuan3d_mode == 'OFFICIAL_API':
                sub.prop(scene, "blendbridge_hunyuan3d_secret_id", text="SecretId")
                sub.prop(scene, "blendbridge_hunyuan3d_secret_key", text="SecretKey")
            if scene.blendbridge_hunyuan3d_mode == 'LOCAL_API':
                sub.prop(scene, "blendbridge_hunyuan3d_api_url", text="API URL")
                sub.prop(scene, "blendbridge_hunyuan3d_octree_resolution", text="Octree Resolution")
                sub.prop(scene, "blendbridge_hunyuan3d_num_inference_steps", text="Inference Steps")
                sub.prop(scene, "blendbridge_hunyuan3d_guidance_scale", text="Guidance Scale")
                sub.prop(scene, "blendbridge_hunyuan3d_texture", text="Generate Texture")


# Operators (preserved from original)
class BLENDBRIDGE_OT_SetFreeTrialHyper3DAPIKey(bpy.types.Operator):
    bl_idname = "blendbridge.set_hyper3d_free_trial_api_key"
    bl_label = "Set Free Trial API Key"

    def execute(self, context):
        context.scene.blendbridge_hyper3d_api_key = RODIN_FREE_TRIAL_KEY
        context.scene.blendbridge_hyper3d_mode = 'MAIN_SITE'
        self.report({'INFO'}, "API Key set successfully!")
        return {'FINISHED'}

class BLENDBRIDGE_OT_StartServer(bpy.types.Operator):
    bl_idname = "blendbridge.start_server"
    bl_label = "Start Bridge"
    bl_description = "Start the blendbridge-mcp socket server for MCP clients"

    def execute(self, context):
        scene = context.scene

        # Create a new server instance using new modular server
        if not hasattr(bpy.types, "blendbridge_server") or not bpy.types.blendbridge_server:
            bpy.types.blendbridge_server = BlendBridgeServer(port=scene.blendbridge_port)

        # Start the server
        bpy.types.blendbridge_server.start()
        scene.blendbridge_server_running = True

        return {'FINISHED'}

class BLENDBRIDGE_OT_StopServer(bpy.types.Operator):
    bl_idname = "blendbridge.stop_server"
    bl_label = "Stop Bridge"
    bl_description = "Stop the blendbridge-mcp socket server"

    def execute(self, context):
        scene = context.scene

        # Stop the server if it exists
        if hasattr(bpy.types, "blendbridge_server") and bpy.types.blendbridge_server:
            bpy.types.blendbridge_server.stop()
            del bpy.types.blendbridge_server

        scene.blendbridge_server_running = False

        return {'FINISHED'}

class BLENDBRIDGE_OT_OpenTerms(bpy.types.Operator):
    bl_idname = "blendbridge.open_terms"
    bl_label = "View Terms and Conditions"
    bl_description = "Open the Terms and Conditions document"

    def execute(self, context):
        terms_url = "https://github.com/ismailubts/blendbridge-mcp/blob/main/TERMS_AND_CONDITIONS.md"
        try:
            import webbrowser
            webbrowser.open(terms_url)
            self.report({'INFO'}, "Terms and Conditions opened in browser")
        except Exception as e:
            self.report({'ERROR'}, f"Could not open Terms and Conditions: {str(e)}")
        
        return {'FINISHED'}

# Registration functions
def register():
    # Register scene properties
    bpy.types.Scene.blendbridge_port = IntProperty(
        name="Port",
        description="Port for the blendbridge-mcp server",
        default=9876,
        min=1024,
        max=65535
    )

    bpy.types.Scene.blendbridge_server_running = bpy.props.BoolProperty(
        name="Server Running",
        default=False
    )

    bpy.types.Scene.blendbridge_use_polyhaven = bpy.props.BoolProperty(
        name="Use Poly Haven",
        description="Enable Poly Haven asset integration",
        default=False
    )

    bpy.types.Scene.blendbridge_use_hyper3d = bpy.props.BoolProperty(
        name="Use Hyper3D Rodin",
        description="Enable Hyper3D Rodin generation integration",
        default=False
    )

    bpy.types.Scene.blendbridge_hyper3d_mode = bpy.props.EnumProperty(
        name="Rodin Mode",
        description="Choose the platform used to call Rodin APIs",
        items=[
            ("MAIN_SITE", "hyper3d.ai", "hyper3d.ai"),
            ("FAL_AI", "fal.ai", "fal.ai"),
        ],
        default="MAIN_SITE"
    )

    bpy.types.Scene.blendbridge_hyper3d_api_key = bpy.props.StringProperty(
        name="Hyper3D API Key",
        subtype="PASSWORD",
        description="API Key provided by Hyper3D",
        default=""
    )

    bpy.types.Scene.blendbridge_use_hunyuan3d = bpy.props.BoolProperty(
        name="Use Hunyuan 3D",
        description="Enable Hunyuan asset integration",
        default=False
    )

    bpy.types.Scene.blendbridge_hunyuan3d_mode = bpy.props.EnumProperty(
        name="Hunyuan3D Mode",
        description="Choose a local or official APIs",
        items=[
            ("LOCAL_API", "local api", "local api"),
            ("OFFICIAL_API", "official api", "official api"),
        ],
        default="LOCAL_API"
    )

    bpy.types.Scene.blendbridge_hunyuan3d_secret_id = bpy.props.StringProperty(
        name="Hunyuan 3D SecretId",
        description="SecretId provided by Hunyuan 3D",
        default=""
    )

    bpy.types.Scene.blendbridge_hunyuan3d_secret_key = bpy.props.StringProperty(
        name="Hunyuan 3D SecretKey",
        subtype="PASSWORD",
        description="SecretKey provided by Hunyuan 3D",
        default=""
    )

    bpy.types.Scene.blendbridge_hunyuan3d_api_url = bpy.props.StringProperty(
        name="API URL",
        description="URL of the Hunyuan 3D API service",
        default="http://localhost:8081"
    )

    bpy.types.Scene.blendbridge_hunyuan3d_octree_resolution = bpy.props.IntProperty(
        name="Octree Resolution",
        description="Octree resolution for the 3D generation",
        default=256,
        min=128,
        max=512,
    )

    bpy.types.Scene.blendbridge_hunyuan3d_num_inference_steps = bpy.props.IntProperty(
        name="Number of Inference Steps",
        description="Number of inference steps for the 3D generation",
        default=20,
        min=20,
        max=50,
    )

    bpy.types.Scene.blendbridge_hunyuan3d_guidance_scale = bpy.props.FloatProperty(
        name="Guidance Scale",
        description="Guidance scale for the 3D generation",
        default=5.5,
        min=1.0,
        max=10.0,
    )

    bpy.types.Scene.blendbridge_hunyuan3d_texture = bpy.props.BoolProperty(
        name="Generate Texture",
        description="Whether to generate texture for the 3D model",
        default=False,
    )
    
    bpy.types.Scene.blendbridge_use_sketchfab = bpy.props.BoolProperty(
        name="Use Sketchfab",
        description="Enable Sketchfab asset integration",
        default=False
    )

    bpy.types.Scene.blendbridge_sketchfab_api_key = bpy.props.StringProperty(
        name="Sketchfab API Key",
        subtype="PASSWORD",
        description="API Key provided by Sketchfab",
        default=""
    )

    # Register classes
    bpy.utils.register_class(BLENDBRIDGE_AddonPreferences)
    bpy.utils.register_class(BLENDBRIDGE_PT_Panel)
    bpy.utils.register_class(BLENDBRIDGE_OT_SetFreeTrialHyper3DAPIKey)
    bpy.utils.register_class(BLENDBRIDGE_OT_StartServer)
    bpy.utils.register_class(BLENDBRIDGE_OT_StopServer)
    bpy.utils.register_class(BLENDBRIDGE_OT_OpenTerms)

    logger.info("blendbridge-mcp addon registered (v2.0)")

def unregister():
    # Stop the server if it's running
    if hasattr(bpy.types, "blendbridge_server") and bpy.types.blendbridge_server:
        bpy.types.blendbridge_server.stop()
        del bpy.types.blendbridge_server

    bpy.utils.unregister_class(BLENDBRIDGE_PT_Panel)
    bpy.utils.unregister_class(BLENDBRIDGE_OT_SetFreeTrialHyper3DAPIKey)
    bpy.utils.unregister_class(BLENDBRIDGE_OT_StartServer)
    bpy.utils.unregister_class(BLENDBRIDGE_OT_StopServer)
    bpy.utils.unregister_class(BLENDBRIDGE_OT_OpenTerms)
    bpy.utils.unregister_class(BLENDBRIDGE_AddonPreferences)

    # Clean up scene properties
    del bpy.types.Scene.blendbridge_port
    del bpy.types.Scene.blendbridge_server_running
    del bpy.types.Scene.blendbridge_use_polyhaven
    del bpy.types.Scene.blendbridge_use_hyper3d
    del bpy.types.Scene.blendbridge_hyper3d_mode
    del bpy.types.Scene.blendbridge_hyper3d_api_key
    del bpy.types.Scene.blendbridge_use_sketchfab
    del bpy.types.Scene.blendbridge_sketchfab_api_key
    del bpy.types.Scene.blendbridge_use_hunyuan3d
    del bpy.types.Scene.blendbridge_hunyuan3d_mode
    del bpy.types.Scene.blendbridge_hunyuan3d_secret_id
    del bpy.types.Scene.blendbridge_hunyuan3d_secret_key
    del bpy.types.Scene.blendbridge_hunyuan3d_api_url
    del bpy.types.Scene.blendbridge_hunyuan3d_octree_resolution
    del bpy.types.Scene.blendbridge_hunyuan3d_num_inference_steps
    del bpy.types.Scene.blendbridge_hunyuan3d_guidance_scale
    del bpy.types.Scene.blendbridge_hunyuan3d_texture

    logger.info("blendbridge-mcp addon unregistered")

if __name__ == "__main__":
    register()
