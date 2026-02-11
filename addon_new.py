# BlendBridge by Aismail (aismail@7kingscode.com) © 2026
# Enhanced with comprehensive BlendBridge system

# bl_info MUST be defined before any imports that might fail
bl_info = {
    "name": "BlendBridge",
    "author": "Aismail (aismail@7kingscode.com)",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > BlendBridge",
    "description": "Bridge Blender to AI assistants through MCP",
    "category": "Interface",
}

import bpy
from bpy.props import IntProperty, BoolProperty
import os
import sys

# Add current directory and parent directory to path for imports
# This handles both single-file and directory installations
blendbridge_mcp_file = os.path.abspath(__file__)
blendbridge_mcp_dir = os.path.dirname(blendbridge_mcp_file)
blendbridge_mcp_parent = os.path.dirname(blendbridge_mcp_dir)

# Add both current directory and parent directory to path
for path in [blendbridge_mcp_dir, blendbridge_mcp_parent]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Additional imports needed for the server
import json
import threading
import socket
import time
import traceback

# Initialize fallback logger first (always available)
class FallbackLogger:
    @staticmethod
    def info(msg):
        print(f"INFO: {msg}")
    @staticmethod
    def error(msg):
        print(f"ERROR: {msg}")
    @staticmethod
    def warning(msg):
        print(f"WARNING: {msg}")
    @staticmethod
    def debug(msg):
        print(f"DEBUG: {msg}")
    @staticmethod
    def exception(msg):
        print(f"EXCEPTION: {msg}")
        traceback.print_exc()

# Define a WORKING fallback server that doesn't depend on modular imports
# This is based on the original addon.py server
class FallbackBlendBridgeServer:
    """Fallback server that works without modular system"""
    
    def __init__(self, host='localhost', port=9876):
        self.host = host
        self.port = port
        self.running = False
        self.socket = None
        self.server_thread = None

    def start(self):
        if self.running:
            print("Server is already running")
            return

        self.running = True

        try:
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)

            # Start server thread
            self.server_thread = threading.Thread(target=self._server_loop)
            self.server_thread.daemon = True
            self.server_thread.start()

            print(f"BlendBridge server started on {self.host}:{self.port}")
        except Exception as e:
            print(f"Failed to start server: {str(e)}")
            self.stop()

    def stop(self):
        self.running = False

        # Close socket
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None

        # Wait for thread to finish
        if self.server_thread:
            try:
                if self.server_thread.is_alive():
                    self.server_thread.join(timeout=1.0)
            except:
                pass
            self.server_thread = None

        print("BlendBridge server stopped")

    def _server_loop(self):
        """Main server loop in a separate thread"""
        print("Server thread started")
        self.socket.settimeout(1.0)

        while self.running:
            try:
                try:
                    client, address = self.socket.accept()
                    print(f"Connected to client: {address}")

                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client,)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Error accepting connection: {str(e)}")
                    time.sleep(0.5)
            except Exception as e:
                print(f"Error in server loop: {str(e)}")
                if not self.running:
                    break
                time.sleep(0.5)

        print("Server thread stopped")

    def _handle_client(self, client):
        """Handle connected client"""
        print("Client handler started")
        client.settimeout(None)
        buffer = b''

        try:
            while self.running:
                try:
                    data = client.recv(8192)
                    if not data:
                        print("Client disconnected")
                        break

                    buffer += data
                    try:
                        command = json.loads(buffer.decode('utf-8'))
                        buffer = b''

                        def execute_wrapper():
                            try:
                                response = self.execute_command(command)
                                response_json = json.dumps(response)
                                try:
                                    client.sendall(response_json.encode('utf-8'))
                                except:
                                    print("Failed to send response - client disconnected")
                            except Exception as e:
                                print(f"Error executing command: {str(e)}")
                                traceback.print_exc()
                                try:
                                    error_response = {
                                        "status": "error",
                                        "message": str(e)
                                    }
                                    client.sendall(json.dumps(error_response).encode('utf-8'))
                                except:
                                    pass
                            return None

                        bpy.app.timers.register(execute_wrapper, first_interval=0.0)
                    except json.JSONDecodeError:
                        pass
                except Exception as e:
                    print(f"Error receiving data: {str(e)}")
                    break
        except Exception as e:
            print(f"Error in client handler: {str(e)}")
        finally:
            try:
                client.close()
            except:
                pass
            print("Client handler stopped")

    def execute_command(self, command):
        """Execute a command - basic implementation"""
        try:
            # Validate command is a dictionary
            if not isinstance(command, dict):
                if isinstance(command, str):
                    # Try to parse if it's a JSON string
                    try:
                        command = json.loads(command)
                    except json.JSONDecodeError:
                        return {
                            "status": "error",
                            "message": f"Command must be a dictionary or valid JSON, got: {type(command).__name__}"
                        }
                else:
                    return {
                        "status": "error",
                        "message": f"Command must be a dictionary, got: {type(command).__name__}"
                    }
            
            # Now safe to use .get()
            cmd_type = command.get("type")
            params = command.get("params", {})
            
            if not cmd_type:
                return {
                    "status": "error",
                    "message": "Command type is required"
                }
            
            # Basic command handling
            if cmd_type == "get_scene_info":
                return self._get_scene_info()
            elif cmd_type == "execute_code":
                return self._execute_code(params.get("code", ""))
            else:
                # Check if modular system is available
                if MODULAR_SYSTEM_AVAILABLE:
                    # Try to use modular system (shouldn't reach here if router works)
                    return {
                        "status": "error",
                        "error": {
                            "code": "HANDLER_NOT_FOUND",
                            "message": f"Command '{cmd_type}' not found. Modular system loaded but handler not registered."
                        }
                    }
                else:
                    return {
                        "status": "error",
                        "error": {
                            "code": "MODULAR_SYSTEM_NOT_LOADED",
                            "message": f"Command '{cmd_type}' requires the modular system. Please ensure core/, handlers/, and utils/ directories are installed."
                        }
                    }
        except Exception as e:
            print(f"Error executing command: {str(e)}")
            traceback.print_exc()
            return {"status": "error", "message": str(e)}
    
    def _get_scene_info(self):
        """Get basic scene information"""
        scene = bpy.context.scene
        objects = []
        for obj in scene.objects:
            objects.append({
                "name": obj.name,
                "type": obj.type,
                "location": list(obj.location),
            })
        return {
            "status": "success",
            "result": {
                "scene_name": scene.name,
                "object_count": len(scene.objects),
                "objects": objects[:50],  # Limit to 50
            }
        }
    
    def _execute_code(self, code):
        """Execute Python code in Blender"""
        try:
            # Create a namespace for execution
            namespace = {"bpy": bpy}
            exec(code, namespace)
            return {"status": "success", "result": "Code executed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Try to import new modular system
# Handle both single-file and directory installations
MODULAR_SYSTEM_AVAILABLE = False
BlendBridgeServer = FallbackBlendBridgeServer  # Default to fallback
register_all_handlers = lambda: None  # Default to no-op
logger = FallbackLogger()  # Initialize with fallback first

try:
    from core.server import BlendBridgeServer as ModularServer
    from handlers.handler_registry import register_all_handlers as modular_register
    from utils.logger import logger as modular_logger
    BlendBridgeServer = ModularServer
    register_all_handlers = modular_register
    logger = modular_logger
    MODULAR_SYSTEM_AVAILABLE = True
    print("BlendBridge: Modular system loaded successfully")
except ImportError as import_error:
    print(f"BlendBridge: Modular system not available ({import_error})")
    print("BlendBridge: Using fallback server with basic functionality")
    # BlendBridgeServer already set to FallbackBlendBridgeServer above

# Import existing integration code (will be preserved)
# This will be handled by creating wrapper handlers

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
# This will be done in the register() function to avoid errors during import

# Blender Addon Preferences (preserved from original)
class BLENDBRIDGE_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    telemetry_consent: BoolProperty(
        name="Allow Anonymized Prompt Collection",
        description="Allow collection of anonymized prompts to help improve BlendBridge",
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
        box.label(text="All data is anonymized and helps improve BlendBridge.", icon='INFO')
        box.label(text="You can opt out anytime by unchecking the box above.", icon='INFO')
        
        # Terms and Conditions link
        box.separator()
        row = box.row()
        row.operator("blendbridge.open_terms", text="View Terms and Conditions", icon='TEXT')

# BlendBridge sidebar panel
class BLENDBRIDGE_PT_Panel(bpy.types.Panel):
    bl_label = "BlendBridge"
    bl_idname = "BLENDBRIDGE_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BlendBridge'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Brand header
        header = layout.box()
        header.label(text="BlendBridge", icon='LINKED')
        header.label(text="AI scene bridge by Aismail")

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
    bl_description = "Start the BlendBridge socket server for MCP clients"

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
    bl_description = "Stop the BlendBridge socket server"

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
        terms_url = "https://github.com/aismail/blendbridge-mcp/blob/main/TERMS_AND_CONDITIONS.md"
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
        description="Port for the BlendBridge server",
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

    # Register all new handlers (only if modular system is available)
    if MODULAR_SYSTEM_AVAILABLE and register_all_handlers is not None:
        try:
            print("BlendBridge: Calling register_all_handlers()...")
            register_all_handlers()
            
            # Verify handlers were registered
            try:
                from core.command_router import command_router
                registered_commands = command_router.get_registered_commands()
                print(f"BlendBridge: Registered {len(registered_commands)} handlers")
                print(f"BlendBridge: Commands: {', '.join(sorted(registered_commands))}")
                
                # Check for specific handlers
                if "get_render_settings" in registered_commands:
                    print("BlendBridge: ✓ Render handlers registered")
                else:
                    print("BlendBridge: ✗ Render handlers NOT registered")
                
                if "get_sketchfab_status" in registered_commands:
                    print("BlendBridge: ✓ Sketchfab handlers registered")
                else:
                    print("BlendBridge: ✗ Sketchfab handlers NOT registered")
            except Exception as verify_error:
                print(f"BlendBridge: Could not verify handlers: {verify_error}")
            
            logger.info("All handlers registered successfully")
            print("BlendBridge: All handlers registered successfully")
        except Exception as e:
            error_msg = f"Error registering handlers: {e}"
            logger.error(error_msg)
            print(f"BlendBridge: {error_msg}")
            import traceback
            traceback.print_exc()
    else:
        print("BlendBridge: Modular system not available - using basic functionality")
        if not MODULAR_SYSTEM_AVAILABLE:
            print("BlendBridge: MODULAR_SYSTEM_AVAILABLE = False")
        if register_all_handlers is None:
            print("BlendBridge: register_all_handlers is None")

    logger.info("BlendBridge addon registered (v2.0)")
    print("BlendBridge addon registered (v2.0)")

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

    logger.info("BlendBridge addon unregistered")
    print("BlendBridge addon unregistered")

if __name__ == "__main__":
    register()
