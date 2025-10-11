#!/usr/bin/env python3
"""Enhanced Core constants for RGB Controller with OSIRIS per-key support"""

import os
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Application Constants
VERSION = "3.0.0-OSIRIS"
APP_NAME = "Enhanced Chromebook RGB Controller"

# Hardware Configuration
NUM_ZONES = 4  # Legacy zone support for compatibility
LEDS_PER_ZONE = 3  # Legacy LEDs per zone
TOTAL_LEDS = NUM_ZONES * LEDS_PER_ZONE  # Legacy total LEDs

# OSIRIS Hardware Constants (New - Primary)
OSIRIS_KEY_COUNT = 100  # Individual addressable keys on OSIRIS hardware
OSIRIS_ROWS = 7  # Approximate keyboard rows
OSIRIS_COLS = 14  # Approximate keyboard columns
OSIRIS_MAX_BRIGHTNESS = 100  # Maximum brightness percentage
OSIRIS_MIN_BRIGHTNESS = 0  # Minimum brightness percentage

# Hardware Detection Constants
HARDWARE_DETECTION_TIMEOUT = 10.0  # seconds
HARDWARE_METHODS = ["ec_direct", "ectool", "none"]
DEFAULT_HARDWARE_METHOD = "ectool"
FALLBACK_HARDWARE_METHOD = "none"

# Animation and Effects Constants
ANIMATION_FRAME_DELAY = 0.033  # ~30 FPS for smooth effects
REACTIVE_DELAY = 1.0  # Default reactive effect duration
MIN_ANIMATION_FRAME_DELAY = 0.016  # ~60 FPS maximum
MAX_ANIMATION_FRAME_DELAY = 0.2  # ~5 FPS minimum
BASE_ANIMATION_DELAY_SPEED_1 = 0.5  # Base delay for slowest speed

# Effect Speed Constants
EFFECT_SPEED_MIN = 1
EFFECT_SPEED_MAX = 10
EFFECT_SPEED_DEFAULT = 5

# Interactive Effect Constants
REACTIVE_FADE_TIME_MIN = 0.1  # Minimum fade time in seconds
REACTIVE_FADE_TIME_MAX = 10.0  # Maximum fade time in seconds
REACTIVE_FADE_TIME_DEFAULT = 1.0  # Default fade time

RIPPLE_SPEED_MIN = 1.0
RIPPLE_SPEED_MAX = 100.0
RIPPLE_SPEED_DEFAULT = 20.0

TRAIL_LENGTH_MIN = 2
TRAIL_LENGTH_MAX = 20
TRAIL_LENGTH_DEFAULT = 8

TYPE_LIGHTING_SPREAD_SPEED_MIN = 1.0
TYPE_LIGHTING_SPREAD_SPEED_MAX = 20.0
TYPE_LIGHTING_SPREAD_SPEED_DEFAULT = 8.0

# System Monitor Constants
SYSTEM_MONITOR_UPDATE_INTERVAL = 1.0  # seconds
CPU_TEMP_MAX_DEFAULT = 80.0  # Celsius
GPU_TEMP_MAX_DEFAULT = 90.0  # Celsius

# Audio Visualizer Constants
AUDIO_SENSITIVITY_MIN = 0.1
AUDIO_SENSITIVITY_MAX = 5.0
AUDIO_SENSITIVITY_DEFAULT = 1.0
AUDIO_SAMPLE_RATE = 44100
AUDIO_BUFFER_SIZE = 1024

# Hardware Interaction Constants
ECTOOL_INTER_COMMAND_DELAY = 0.02  # Delay between ectool commands
ECTOOL_TIMEOUT = 5.0  # Timeout for ectool commands
EC_DIRECT_TIMEOUT = 2.0  # Timeout for EC direct operations

# Error Handling Constants
MAX_RETRY_ATTEMPTS = 3
RETRY_DELAY_BASE = 0.5  # seconds
MAX_ERROR_COUNT = 10
CIRCUIT_BREAKER_THRESHOLD = 5
CIRCUIT_BREAKER_TIMEOUT = 30  # seconds

# Preview Configuration
PREVIEW_WIDTH = 560  # Wider for 100-key layout
PREVIEW_HEIGHT = 200  # Taller for keyboard representation
PREVIEW_KEYBOARD_COLOR = "#1a1a1a"
PREVIEW_KEY_SIZE = 18  # Individual key size
PREVIEW_KEY_SPACING = 2  # Spacing between keys
PREVIEW_KEY_RADIUS = 3  # Rounded corners for keys
PREVIEW_BACKGROUND_COLOR = "#0d1117"
PREVIEW_BORDER_COLOR = "#30363d"

# File path management
def get_app_config_dir() -> Path:
    """Gets the application's configuration directory, preferring XDG standards."""
    app_name_fs = APP_NAME.lower().replace(" ", "_").replace("-", "_")

    xdg_config_home_str = os.environ.get('XDG_CONFIG_HOME')
    if xdg_config_home_str and Path(xdg_config_home_str).is_dir():
        base_path = Path(xdg_config_home_str)
    pass
    else:
    pass
    pass
    pass
        base_path = Path.home() / ".config"
        if os.name == 'nt':  # Windows
            appdata = os.environ.get('APPDATA')
            if appdata:
        base_path = Path(appdata)
    pass
            else:
    pass
    pass
    pass
        base_path = Path.home() / "AppData" / "Roaming"

    return base_path / app_name_fs

# File paths
APP_CONFIG_BASE_DIR = get_app_config_dir()
CONFIG_DIR = APP_CONFIG_BASE_DIR
LOG_DIR = APP_CONFIG_BASE_DIR / "logs"
BACKUP_DIR = APP_CONFIG_BASE_DIR / "backups"
EXPORT_DIR = APP_CONFIG_BASE_DIR / "exports"
CACHE_DIR = APP_CONFIG_BASE_DIR / "cache"
SETTINGS_FILE = APP_CONFIG_BASE_DIR / "settings.json"
DESKTOP_FILE_NAME = f"{APP_NAME.lower().replace(' ', '-')}.desktop"

# Effect Categories (matching library.py)
EFFECT_CATEGORIES = {
    "Static Effects": ["Static Color"],
    "Color Transitions": ["Color Shift", "Color Cycle", "Breathing", "Rainbow Wave", "Aurora"],
    "Interactive Effects": [
        "Reactive Keypress", "Fade on Press", "Ripple", "Trail",
        "Type Lighting (Row)", "Type Lighting (Column)"
    ],
    "Wave & Motion": ["Pulse Wave", "Scanning Beam", "Snake", "Ocean"],
    "Particle & Weather": [
        "Meteor", "Fire", "Lava", "Starlight", "Rain", "Snowfall",
        "Lightning", "Galaxy", "Matrix Code"
    ],
    "System Integration": ["Audio Visualizer", "System Monitor", "Temperature Monitor"],
    "Utility Effects": ["Countdown"]
}

# Default color palette for effects
DEFAULT_EFFECT_COLORS = {
    "primary": "#FF0064",      # Bright pink/magenta
    "secondary": "#00FF64",    # Bright green
    "accent": "#6400FF",       # Purple
    "warning": "#FF6400",      # Orange
    "error": "#FF0000",        # Red
    "success": "#00FF00",      # Green
    "info": "#0064FF",         # Blue
    "neutral": "#FFFFFF",      # White
    "background": "#000000",   # Black
    "osiris_optimal": "#FFFF64"  # Yellow-white (optimal for OSIRIS brightness)
}

# OSIRIS-specific presets
OSIRIS_BRIGHTNESS_PRESETS = {
    "dim": 25,
    "medium": 50,
    "bright": 75,
    "maximum": 100,
    "auto": -1  # Auto-adjust based on ambient light if available
}

# Effect presets for quick access
EFFECT_PRESETS = {
    "gaming": {
        "effect_name": "Reactive Keypress",
        "color": DEFAULT_EFFECT_COLORS["primary"],
        "speed": 8,
        "brightness": 90
    },
    "productivity": {
        "effect_name": "Breathing",
        "color": DEFAULT_EFFECT_COLORS["info"],
        "speed": 3,
        "brightness": 60
    },
    "ambient": {
        "effect_name": "Aurora",
        "speed": 2,
        "brightness": 40
    },
    "party": {
        "effect_name": "Rainbow Wave",
        "speed": 7,
        "brightness": 100
    },
    "focus": {
        "effect_name": "Static Color",
        "color": DEFAULT_EFFECT_COLORS["neutral"],
        "brightness": 30
    }
}

# Enhanced default settings with all new effects support
default_settings: Dict[str, Any] = {
    # Basic settings
    'brightness': OSIRIS_MAX_BRIGHTNESS,
    'current_color': {"r": 255, "g": 0, "b": 100},  # Bright pink

    # Zone colors (legacy compatibility)
    'zone_colors': [
        {"r": 255, "g": 0, "b": 100},    # Zone 1 (Pink)
        {"r": 0, "g": 255, "b": 100},    # Zone 2 (Green-cyan)
        {"r": 100, "g": 0, "b": 255},    # Zone 3 (Purple)
        {"r": 255, "g": 100, "b": 0}     # Zone 4 (Orange)
    ],

    # Effect settings
    'effect_name': "Static Color",
    'effect_speed': EFFECT_SPEED_DEFAULT,
    'effect_color': DEFAULT_EFFECT_COLORS["primary"],
    'effect_rainbow_mode': False,
    'gradient_start_color': DEFAULT_EFFECT_COLORS["primary"],
    'gradient_end_color': DEFAULT_EFFECT_COLORS["secondary"],
    'effect_background_color': DEFAULT_EFFECT_COLORS["background"],

    # Interactive effect settings
    'reactive_fade_time': REACTIVE_FADE_TIME_DEFAULT,
    'ripple_speed': RIPPLE_SPEED_DEFAULT,
    'trail_length': TRAIL_LENGTH_DEFAULT,
    'type_lighting_spread_speed': TYPE_LIGHTING_SPREAD_SPEED_DEFAULT,

    # System integration settings
    'audio_sensitivity': AUDIO_SENSITIVITY_DEFAULT,
    'system_monitor_type': "cpu",
    'temperature_monitor_enabled': False,
    'temperature_max_threshold': CPU_TEMP_MAX_DEFAULT,

    # Hardware settings
    'last_control_method': DEFAULT_HARDWARE_METHOD,
    'hardware_detection_enabled': True,
    'osiris_optimization': True,

    # Application behavior
    'restore_on_startup': True,
    'auto_apply_last_setting': True,
    'last_mode': "static",
    'clean_shutdown': False,
    'minimize_to_tray': False,  # Changed to False for better UX
    'keep_effects_running': True,
    'auto_brightness_adjustment': False,
    'performance_mode': "balanced",  # "low", "balanced", "high"

    # GUI settings
    'window_width': 800,
    'window_height': 600,
    'theme': "dark",
    'show_advanced_options': False,
    'preview_enabled': True,
    'preview_realtime': True,

    # Effect categories visibility
    'visible_categories': list(EFFECT_CATEGORIES.keys()),

    # Keyboard layout
    'keyboard_layout': "qwerty",
    'key_labels_visible': True,

    # Performance settings
    'max_fps': 30,
    'reduce_animations_on_battery': True,
    'hardware_acceleration': True,

    # Safety settings
    'brightness_limit_enabled': False,
    'brightness_limit_value': 80,
    'temperature_protection_enabled': True,
    'safe_mode_on_error': True,

    # Accessibility
    'high_contrast_mode': False,
    'reduce_motion': False,
    'screen_reader_support': False,

    # Advanced features
    'developer_mode': False,
    'debug_logging': False,
    'telemetry_enabled': False,
    'auto_updates_enabled': True,

    # Session data
    'last_used_preset': None,
    'favorite_effects': [],
    'usage_statistics': {},
    'first_run': True,
    'setup_completed': False
}

# Ensure zone_colors has exactly NUM_ZONES entries
_default_zone_colors = default_settings['zone_colors']
if len(_default_zone_colors) != NUM_ZONES:
    default_settings['zone_colors'] = [
    pass
        _default_zone_colors[i % len(_default_zone_colors)]
        for i in range(NUM_ZONES)
    ]

# Keyboard layout mapping for OSIRIS (100 keys)
OSIRIS_KEY_LAYOUT = {
    # Function row (Row 0)
    0: "F1", 1: "F2", 2: "F3", 3: "F4", 4: "F5", 5: "F6", 6: "F7", 7: "F8", 8: "F9", 9: "F10",

    # Number row (Row 1)
    10: "`", 11: "1", 12: "2", 13: "3", 14: "4", 15: "5", 16: "6", 17: "7", 18: "8", 19: "9", 20: "0",
    21: "-", 22: "=", 23: "Backspace",

    # QWERTY row (Row 2)
    24: "Tab", 25: "Q", 26: "W", 27: "E", 28: "R", 29: "T", 30: "Y", 31: "U", 32: "I", 33: "O",
    34: "P", 35: "[", 36: "]", 37: "\\",

    # ASDF row (Row 3)
    38: "Caps", 39: "A", 40: "S", 41: "D", 42: "F", 43: "G", 44: "H", 45: "J", 46: "K", 47: "L",
    48: ";", 49: "'", 50: "Enter",

    # ZXCV row (Row 4)
    51: "LShift", 52: "Z", 53: "X", 54: "C", 55: "V", 56: "B", 57: "N", 58: "M", 59: ",", 60: ".",
    61: "/", 62: "RShift",

    # Bottom row (Row 5)
    63: "LCtrl", 64: "Fn", 65: "LAlt", 66: "Space", 67: "RAlt", 68: "RCtrl",

    # Arrow cluster and navigation (Row 6)
    69: "Up", 70: "Down", 71: "Left", 72: "Right", 73: "Home", 74: "End", 75: "PgUp", 76: "PgDn",
    77: "Insert", 78: "Delete", 79: "PrtScr", 80: "ScrLk", 81: "Pause",

    # Extra zones for full coverage (Row 6 continued)
    **{i: f"Extra{i-82}" for i in range(82, 100)}  # Extra0-17 for zones 82-99
}

# Reverse lookup for key names to IDs
OSIRIS_KEY_NAME_TO_ID = {v: k for k, v in OSIRIS_KEY_LAYOUT.items()}

# Key groupings for effect targeting
KEY_GROUPS = {
    "function_keys": list(range(0, 10)),
    "number_row": list(range(10, 24)),
    "qwerty_row": list(range(24, 38)),
    "asdf_row": list(range(38, 51)),
    "zxcv_row": list(range(51, 63)),
    "bottom_row": list(range(63, 69)),
    "arrow_cluster": list(range(69, 73)),
    "navigation": list(range(73, 82)),
    "extra_zones": list(range(82, 100)),
    "all_keys": list(range(OSIRIS_KEY_COUNT)),
    "main_alpha": list(range(25, 51)) + list(range(52, 62)),  # Main typing keys
    "modifiers": [38, 51, 62, 63, 64, 65, 67, 68],  # Caps, Shifts, Ctrl, Fn, Alt
    "space_area": [66],  # Just spacebar
}

# Hardware compatibility matrix
HARDWARE_COMPATIBILITY = {
    "ec_direct": {
        "supports_per_key": True,
        "supports_zones": True,
        "supports_brightness": True,
        "supports_reactive": True,
        "max_update_rate": 30,  # Hz
        "requires_root": True,
        "platform_support": ["linux"],
        "hardware_support": ["osiris", "chromebook"]
    },
    "ectool": {
        "supports_per_key": True,
        "supports_zones": True,
        "supports_brightness": True,
        "supports_reactive": False,  # Limited by command overhead
        "max_update_rate": 10,  # Hz
        "requires_root": True,
        "platform_support": ["linux"],
        "hardware_support": ["osiris", "chromebook", "generic"]
    },
    "none": {
        "supports_per_key": False,
        "supports_zones": False,
        "supports_brightness": False,
        "supports_reactive": False,
        "max_update_rate": 0,
        "requires_root": False,
        "platform_support": ["linux", "windows", "macos"],
        "hardware_support": []
    }
}

# Effect compatibility with hardware
EFFECT_HARDWARE_REQUIREMENTS = {
    # Low requirement effects (work on all hardware)
    "Static Color": {"min_update_rate": 1, "requires_reactive": False},
    "Breathing": {"min_update_rate": 5, "requires_reactive": False},
    "Color Shift": {"min_update_rate": 10, "requires_reactive": False},
    "Color Cycle": {"min_update_rate": 5, "requires_reactive": False},

    # Medium requirement effects
    "Rainbow Wave": {"min_update_rate": 15, "requires_reactive": False},
    "Scanning Beam": {"min_update_rate": 10, "requires_reactive": False},
    "Snake": {"min_update_rate": 15, "requires_reactive": False},
    "Aurora": {"min_update_rate": 20, "requires_reactive": False},

    # High requirement effects (need fast updates)
    "Fire": {"min_update_rate": 20, "requires_reactive": False},
    "Lava": {"min_update_rate": 20, "requires_reactive": False},
    "Ocean": {"min_update_rate": 25, "requires_reactive": False},
    "Matrix Code": {"min_update_rate": 20, "requires_reactive": False},

    # Interactive effects (require keypress detection)
    "Reactive Keypress": {"min_update_rate": 30, "requires_reactive": True},
    "Fade on Press": {"min_update_rate": 30, "requires_reactive": True},
    "Ripple": {"min_update_rate": 30, "requires_reactive": True},
    "Trail": {"min_update_rate": 30, "requires_reactive": True},
    "Type Lighting (Row)": {"min_update_rate": 30, "requires_reactive": True},
    "Type Lighting (Column)": {"min_update_rate": 30, "requires_reactive": True},

    # System integration effects
    "Audio Visualizer": {"min_update_rate": 25, "requires_reactive": False},
    "System Monitor": {"min_update_rate": 5, "requires_reactive": False},
    "Temperature Monitor": {"min_update_rate": 1, "requires_reactive": False},
}

# Logging configuration
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
DEFAULT_LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
MAX_LOG_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_LOG_FILES = 5

# Version and update information
MIN_PYTHON_VERSION = (3, 8)
RECOMMENDED_PYTHON_VERSION = (3, 11)
CONFIG_VERSION = "3.0"  # For settings migration
API_VERSION = "v3"

# Export commonly used constants for easy importing
__all__ = [
    # Application
    'VERSION', 'APP_NAME',

    # Hardware
    'OSIRIS_KEY_COUNT', 'OSIRIS_ROWS', 'OSIRIS_COLS',
    'HARDWARE_METHODS', 'HARDWARE_COMPATIBILITY',
    'NUM_ZONES', 'TOTAL_LEDS',  # Legacy compatibility

    # Animation
    'ANIMATION_FRAME_DELAY', 'REACTIVE_DELAY',
    'EFFECT_SPEED_MIN', 'EFFECT_SPEED_MAX', 'EFFECT_SPEED_DEFAULT',

    # Colors and presets
    'DEFAULT_EFFECT_COLORS', 'EFFECT_PRESETS', 'OSIRIS_BRIGHTNESS_PRESETS',

    # File paths
    'CONFIG_DIR', 'LOG_DIR', 'SETTINGS_FILE', 'BACKUP_DIR',

    # Settings
    'default_settings',

    # Layout
    'OSIRIS_KEY_LAYOUT', 'KEY_GROUPS',

    # Effects
    'EFFECT_CATEGORIES', 'EFFECT_HARDWARE_REQUIREMENTS',

    # Constants for effects
    'REACTIVE_FADE_TIME_DEFAULT', 'RIPPLE_SPEED_DEFAULT', 'TRAIL_LENGTH_DEFAULT'
]
