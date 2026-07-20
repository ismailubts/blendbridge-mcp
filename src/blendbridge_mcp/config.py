"""Telemetry configuration for blendbridge-mcp."""

from dataclasses import dataclass


@dataclass
class TelemetryConfig:
    enabled: bool = True
    # Optional Supabase credentials; leave empty to keep telemetry local-only
    supabase_url: str = ""
    supabase_key: str = ""


telemetry_config = TelemetryConfig()
