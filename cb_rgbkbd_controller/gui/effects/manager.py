#!/usr/bin/env python3
"""Enhanced Effects Manager with OSIRIS optimization and comprehensive effect management"""

import threading
import time
import logging
from typing import Dict, Any, Optional, List, Callable
import queue

from ..core.rgb_color import RGBColor, Colors
from ..core.constants import NUM_ZONES, ANIMATION_FRAME_DELAY
from ..core.exceptions import EffectError, HardwareError
from ..utils.decorators import safe_execute, thread_safe, performance_monitor
from ..utils.input_validation import SafeInputValidation
from .library import BaseEffect, EffectLibrary, effect_library


class EffectManager:
    """
    Enhanced Effects Manager with hardware integration and OSIRIS optimization

    Manages effect execution, transitions, and hardware communication with
    thread-safe operations and comprehensive error handling.
    """

    def __init__(self, hardware_controller=None, parent_logger=None):
        """
        Initialize effect manager

        Args:
            hardware_controller: Hardware controller instance
            parent_logger: Parent logger instance
        """
        self.logger = (parent_logger.getChild('EffectManager')
        if parent_logger else logging.getLogger('EffectManager'))

        self.hardware = hardware_controller
        self._lock = threading.RLock()

        # Effect management
        self.current_effect: Optional[BaseEffect] = None
        self.effect_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()

        # Frame management
        self._frame_queue = queue.Queue(maxsize=60)  # Buffer for 60 frames
        self._frame_counter = 0
        self._effect_start_time = 0.0

        # Performance tracking
        self._frame_times = []
        self._max_frame_time_samples = 100

        # OSIRIS optimization
        self.osiris_mode = False
        self.single_zone_hardware = False

        # State management
        self.is_running = False
        self.last_colors = [Colors.BLACK] * NUM_ZONES

        self.logger.info("Effect Manager initialized")

    def set_hardware_controller(self, hardware_controller):
        """Set or update hardware controller"""
        with self._lock:
            self.hardware = hardware_controller
    pass

            # Detect OSIRIS hardware
            if hasattr(self.hardware, 'is_osiris_hardware'):
        self.osiris_mode = getattr(self.hardware, 'is_osiris_hardware', False)
    pass
        self.single_zone_hardware = self.osiris_mode

        if self.osiris_mode:
        self.logger.info("OSIRIS hardware detected - enabling optimizations")
    pass

    @safe_execute(max_attempts=2, severity="error")
    def start_effect(self, effect_name: str, **kwargs) -> bool:
        """
        Start a lighting effect

        Args:
            effect_name: Name of effect to start
            **kwargs: Effect parameters

        Returns:
            bool: True if effect started successfully
        """
        with self._lock:
            try:
    pass
    pass
    pass
    pass
except:
    pass
            try:
    pass
    pass
    pass
    pass
except:
    pass
        try:
    pass
    pass
    pass
    pass
except:
    pass
        try:
    pass
    pass
    pass
    pass
except:
    pass
        try:
    pass
    pass
    pass
    pass
except:
    pass
        try:
    pass
    pass
    pass
    pass
except:
    pass
        try:
    pass
    pass
    pass
    pass
except:
    pass
        try:
    pass
    pass
    pass
    pass
except:
    pass
        try:
    pass
    pass
    pass
    pass
except:
    pass
        try:
    pass
    pass
    pass
    pass
except:
    pass
# Convenience functions for common operations
def create_effect_manager(hardware_controller=None, logger=None) -> EffectManager:
    """Create effect manager instance"""
    return EffectManager(hardware_controller, logger)


def get_recommended_effects_for_hardware(is_osiris: bool = False) -> List[str]:
    """Get recommended effects for specific hardware"""
    if is_osiris:
        from .library import get_osiris_recommended_effects
    pass
        return get_osiris_recommended_effects()
    else:
    pass
    pass
    pass
        return effect_library.get_available_effects()


def validate_effect_parameters(effect_name: str, **kwargs) -> Dict[str, Any]:
    """Validate effect parameters"""
    validated = {}

    # Common parameter validation
    if 'speed' in kwargs:
        validated['speed'] = SafeInputValidation.validate_speed(kwargs['speed'], default=5)
    pass

    if 'brightness' in kwargs:
        validated['brightness'] = SafeInputValidation.validate_brightness(kwargs['brightness'], default=100)
    pass

    if 'color' in kwargs:
        validated['color'] = SafeInputValidation.validate_color(kwargs['color'], default=Colors.WHITE)
    pass

    if 'colors' in kwargs:
        validated['colors'] = SafeInputValidation.validate_color_list(kwargs['colors'])
    pass

    # Add other parameters as-is
    for key, value in kwargs.items():
        if key not in validated:
    pass
            validated[key] = value

    return validated
