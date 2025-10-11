"""Enhanced Core constants for RGB Controller with OSIRIS per-key support"""
import os
from pathlib import Path
from typing import Dict, Any, List, Tuple
VERSION = '3.0.0-OSIRIS'
APP_NAME = 'Enhanced Chromebook RGB Controller'
NUM_ZONES = 4
LEDS_PER_ZONE = 3
TOTAL_LEDS = NUM_ZONES * LEDS_PER_ZONE
OSIRIS_KEY_COUNT = 100
OSIRIS_ROWS = 7
OSIRIS_COLS = 14
OSIRIS_MAX_BRIGHTNESS = 100
OSIRIS_MIN_BRIGHTNESS = 0
HARDWARE_DETECTION_TIMEOUT = 10.0
HARDWARE_METHODS = ['ec_direct', 'ectool', 'none']
DEFAULT_HARDWARE_METHOD = 'ectool'
FALLBACK_HARDWARE_METHOD = 'none'
ANIMATION_FRAME_DELAY = 0.033
REACTIVE_DELAY = 1.0
MIN_ANIMATION_FRAME_DELAY = 0.016
MAX_ANIMATION_FRAME_DELAY = 0.2
BASE_ANIMATION_DELAY_SPEED_1 = 0.5
EFFECT_SPEED_MIN = 1
EFFECT_SPEED_MAX = 10
EFFECT_SPEED_DEFAULT = 5
REACTIVE_FADE_TIME_MIN = 0.1
REACTIVE_FADE_TIME_MAX = 10.0
REACTIVE_FADE_TIME_DEFAULT = 1.0
RIPPLE_SPEED_MIN = 1.0
RIPPLE_SPEED_MAX = 100.0
RIPPLE_SPEED_DEFAULT = 20.0
TRAIL_LENGTH_MIN = 2
TRAIL_LENGTH_MAX = 20
TRAIL_LENGTH_DEFAULT = 8
TYPE_LIGHTING_SPREAD_SPEED_MIN = 1.0
TYPE_LIGHTING_SPREAD_SPEED_MAX = 20.0
TYPE_LIGHTING_SPREAD_SPEED_DEFAULT = 8.0
SYSTEM_MONITOR_UPDATE_INTERVAL = 1.0
CPU_TEMP_MAX_DEFAULT = 80.0
GPU_TEMP_MAX_DEFAULT = 90.0
AUDIO_SENSITIVITY_MIN = 0.1
AUDIO_SENSITIVITY_MAX = 5.0
AUDIO_SENSITIVITY_DEFAULT = 1.0
AUDIO_SAMPLE_RATE = 44100
AUDIO_BUFFER_SIZE = 1024
ECTOOL_INTER_COMMAND_DELAY = 0.02
ECTOOL_TIMEOUT = 5.0
EC_DIRECT_TIMEOUT = 2.0
MAX_RETRY_ATTEMPTS = 3
RETRY_DELAY_BASE = 0.5
MAX_ERROR_COUNT = 10
CIRCUIT_BREAKER_THRESHOLD = 5
CIRCUIT_BREAKER_TIMEOUT = 30
PREVIEW_WIDTH = 560
PREVIEW_HEIGHT = 200
PREVIEW_KEYBOARD_COLOR = '#1a1a1a'
PREVIEW_KEY_SIZE = 18
PREVIEW_KEY_SPACING = 2
PREVIEW_KEY_RADIUS = 3
PREVIEW_LED_SIZE = 8
PREVIEW_LED_SPACING = 2
PREVIEW_BACKGROUND_COLOR = '#0d1117'
PREVIEW_BORDER_COLOR = '#30363d'

def get_app_config_dir() -> Path:
    """Gets the application's configuration directory, preferring XDG standards."""
    app_name_fs = APP_NAME.lower().replace(' ', '_').replace('-', '_')
    xdg_config_home_str = os.environ.get('XDG_CONFIG_HOME')
    if xdg_config_home_str and Path(xdg_config_home_str).is_dir():
        base_path = Path(xdg_config_home_str)
    else:
        base_path = Path.home() / '.config'
        if os.name == 'nt':
            appdata = os.environ.get('APPDATA')
            if appdata:
                base_path = Path(appdata)
            else:
                base_path = Path.home() / 'AppData' / 'Roaming'
APP_CONFIG_BASE_DIR = get_app_config_dir()
CONFIG_DIR = APP_CONFIG_BASE_DIR
LOG_DIR = APP_CONFIG_BASE_DIR / 'logs'
BACKUP_DIR = APP_CONFIG_BASE_DIR / 'backups'
EXPORT_DIR = APP_CONFIG_BASE_DIR / 'exports'
CACHE_DIR = APP_CONFIG_BASE_DIR / 'cache'
SETTINGS_FILE = APP_CONFIG_BASE_DIR / 'settings.json'
DESKTOP_FILE_NAME = f'{APP_NAME.lower().replace(' ', '-')}.desktop'
EFFECT_CATEGORIES = {'Static Effects': ['Static Color'], 'Color Transitions': ['Color Shift', 'Color Cycle', 'Breathing', 'Rainbow Wave', 'Aurora'], 'Interactive Effects': ['Reactive Keypress', 'Fade on Press', 'Ripple', 'Trail', 'Type Lighting (Row)', 'Type Lighting (Column)'], 'Wave & Motion': ['Pulse Wave', 'Scanning Beam', 'Snake', 'Ocean'], 'Particle & Weather': ['Meteor', 'Fire', 'Lava', 'Starlight', 'Rain', 'Snowfall', 'Lightning', 'Galaxy', 'Matrix Code'], 'System Integration': ['Audio Visualizer', 'System Monitor', 'Temperature Monitor'], 'Utility Effects': ['Countdown']}
DEFAULT_EFFECT_COLORS = {'primary': '#FF0064', 'secondary': '#00FF64', 'accent': '#6400FF', 'warning': '#FF6400', 'error': '#FF0000', 'success': '#00FF00', 'info': '#0064FF', 'neutral': '#FFFFFF', 'background': '#000000', 'osiris_optimal': '#FFFF64'}
OSIRIS_BRIGHTNESS_PRESETS = {'dim': 25, 'medium': 50, 'bright': 75, 'maximum': 100, 'auto': -1}
EFFECT_PRESETS = {'gaming': {'effect_name': 'Reactive Keypress', 'color': DEFAULT_EFFECT_COLORS['primary'], 'speed': 8, 'brightness': 90}, 'productivity': {'effect_name': 'Breathing', 'color': DEFAULT_EFFECT_COLORS['info'], 'speed': 3, 'brightness': 60}, 'ambient': {'effect_name': 'Aurora', 'speed': 2, 'brightness': 40}, 'party': {'effect_name': 'Rainbow Wave', 'speed': 7, 'brightness': 100}, 'focus': {'effect_name': 'Static Color', 'color': DEFAULT_EFFECT_COLORS['neutral'], 'brightness': 30}}
default_settings: Dict[str, Any] = {'brightness': OSIRIS_MAX_BRIGHTNESS, 'current_color': {'r': 255, 'g': 0, 'b': 100}, 'zone_colors': [{'r': 255, 'g': 0, 'b': 100}, {'r': 0, 'g': 255, 'b': 100}, {'r': 100, 'g': 0, 'b': 255}, {'r': 255, 'g': 100, 'b': 0}], 'effect_name': 'Static Color', 'effect_speed': EFFECT_SPEED_DEFAULT, 'effect_color': DEFAULT_EFFECT_COLORS['primary'], 'effect_rainbow_mode': False, 'gradient_start_color': DEFAULT_EFFECT_COLORS['primary'], 'gradient_end_color': DEFAULT_EFFECT_COLORS['secondary'], 'effect_background_color': DEFAULT_EFFECT_COLORS['background'], 'reactive_fade_time': REACTIVE_FADE_TIME_DEFAULT, 'ripple_speed': RIPPLE_SPEED_DEFAULT, 'trail_length': TRAIL_LENGTH_DEFAULT, 'type_lighting_spread_speed': TYPE_LIGHTING_SPREAD_SPEED_DEFAULT, 'audio_sensitivity': AUDIO_SENSITIVITY_DEFAULT, 'system_monitor_type': 'cpu', 'temperature_monitor_enabled': False, 'temperature_max_threshold': CPU_TEMP_MAX_DEFAULT, 'last_control_method': DEFAULT_HARDWARE_METHOD, 'hardware_detection_enabled': True, 'osiris_optimization': True, 'restore_on_startup': True, 'auto_apply_last_setting': True, 'last_mode': 'static', 'clean_shutdown': False, 'minimize_to_tray': False, 'keep_effects_running': True, 'auto_brightness_adjustment': False, 'performance_mode': 'balanced', 'window_width': 800, 'window_height': 600, 'theme': 'dark', 'show_advanced_options': False, 'preview_enabled': True, 'preview_realtime': True, 'visible_categories': list(EFFECT_CATEGORIES.keys()), 'keyboard_layout': 'qwerty', 'key_labels_visible': True, 'max_fps': 30, 'reduce_animations_on_battery': True, 'hardware_acceleration': True, 'brightness_limit_enabled': False, 'brightness_limit_value': 80, 'temperature_protection_enabled': True, 'safe_mode_on_error': True, 'high_contrast_mode': False, 'reduce_motion': False, 'screen_reader_support': False, 'developer_mode': False, 'debug_logging': False, 'telemetry_enabled': False, 'auto_updates_enabled': True, 'last_used_preset': None, 'favorite_effects': [], 'usage_statistics': {}}