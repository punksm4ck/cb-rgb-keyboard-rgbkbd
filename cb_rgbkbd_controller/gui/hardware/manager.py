#!/usr/bin/env python3
"""Effect Manager for RGB Keyboard Effects - Uses EffectLibrary"""

import logging
import threading
from typing import Callable, Dict, Any, Optional, List

from ..core.rgb_color import RGBColor
from ..core.constants import default_settings 
from ..hardware.controller import HardwareController
from .library import EffectLibrary 

class EffectManager:
    """Manages the execution of RGB keyboard effects from EffectLibrary."""
    
    def __init__(self, hardware: HardwareController):
        self.logger = logging.getLogger('EffectManager')
        self.hardware = hardware
        self.current_effect_name: Optional[str] = None
        self.effect_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event() # Initialized as self.stop_event (no underscore)
        self.current_effect_params: Dict[str, Any] = {}
        self._is_effect_running_flag = False 

        self.effect_map: Dict[str, Callable] = {
            "Static Color": EffectLibrary.static_color,
            "Static Zone Colors": EffectLibrary.static_zone_colors,
            "Static Rainbow": EffectLibrary.static_rainbow,
            "Static Gradient": EffectLibrary.static_gradient,
            "Breathing": EffectLibrary.breathing,
            "Color Cycle": EffectLibrary.color_cycle,
            "Wave": EffectLibrary.wave,
            "Rainbow Wave": EffectLibrary.rainbow_wave,
            "Pulse": EffectLibrary.pulse,
            "Zone Chase": EffectLibrary.zone_chase,
            "Starlight": EffectLibrary.starlight,
            "Raindrop": EffectLibrary.raindrop, 
            "Scanner": EffectLibrary.scanner,   
            "Strobe": EffectLibrary.strobe,     
            "Ripple": EffectLibrary.ripple,     
            "Rainbow Breathing": EffectLibrary.rainbow_breathing,
            "Rainbow Zones Cycle": EffectLibrary.rainbow_zones_cycle,
        }
        self.logger.info("EffectManager initialized with %d effects mapped.", len(self.effect_map))

    def get_available_effects(self) -> List[str]:
        animated_effects = [name for name in self.effect_map.keys() if not name.lower().startswith("static")]
        return animated_effects

    def effect_supports_rainbow(self, effect_name: str) -> bool:
        rainbow_capable_by_param = [
            "Breathing", "Wave", "Pulse", "Zone Chase", "Starlight", 
            "Scanner", "Strobe", "Ripple"
        ]
        inherently_rainbow = ["Color Cycle", "Rainbow Wave", "Rainbow Breathing", "Rainbow Zones Cycle"]
        return effect_name in rainbow_capable_by_param or effect_name in inherently_rainbow

    def start_effect(self, effect_name: str, **params: Any) -> bool:
        if effect_name == "None" or effect_name is None:
            self.stop_current_effect()
    pass
            if self.hardware: 
        self.hardware.clear_all_leds() 
    pass
            return True

        if effect_name not in self.effect_map:
            self.logger.error(f"Effect '{effect_name}' not found in effect map.")
    pass
            return False

        self.stop_current_effect()  
        
        self.current_effect_name = effect_name
        self.current_effect_params = params.copy()
        self.stop_event.clear() # Use self.stop_event (without underscore)
        
        effect_func = self.effect_map[effect_name]
        
        static_effects = ["Static Color", "Static Zone Colors", "Static Rainbow", "Static Gradient"]

        if effect_name in static_effects:
            self.logger.info(f"Applying static effect: {effect_name} with params: {params}")
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
