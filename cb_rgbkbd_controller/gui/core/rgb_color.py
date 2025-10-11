"""Enhanced RGB Color class with OSIRIS optimization and comprehensive validation"""
import re
import colorsys
import math
from typing import Union, Tuple, Dict, Any, Optional, List
import json

class RGBColor:
    """RGBColor class"""
    MIN_VALUE = 0
    MAX_VALUE = 255
    HEX_PATTERN = re.compile('^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    LUMINANCE_RED = 0.2126
    LUMINANCE_GREEN = 0.7152
    LUMINANCE_BLUE = 0.0722
    NTSC_LUMINANCE_RED = 0.299
    NTSC_LUMINANCE_GREEN = 0.587
    NTSC_LUMINANCE_BLUE = 0.114

    def __init__(self, r: int=0, g: int=0, b: int=0):
        self._r = self._validate_component(r, 'red')
        self._g = self._validate_component(g, 'green')
        self._b = self._validate_component(b, 'blue')

    def _validate_component(self, value: Union[int, float], component_name: str='component') -> int:
        if not isinstance(value, (int, float)):
            raise ValueError(f'{component_name} must be a number')
        if not self.MIN_VALUE <= int(value) <= self.MAX_VALUE:
            raise ValueError(f'{component_name} must be between {self.MIN_VALUE} and {self.MAX_VALUE}')
        return int(value)

    @property
    def r(self) -> int:
        return self._r

    @r.setter
    def r(self, value: int):
        self._r = self._validate_component(value, 'red')

    @property
    def g(self) -> int:
        return self._g

    @g.setter
    def g(self, value: int):
        self._g = self._validate_component(value, 'green')

    @property
    def b(self) -> int:
        return self._b

    @b.setter
    def b(self, value: int):
        self._b = self._validate_component(value, 'blue')

class Colors:
    """Colors class"""
    BLACK = RGBColor(0, 0, 0)
    WHITE = RGBColor(255, 255, 255)
    RED = RGBColor(255, 0, 0)
    GREEN = RGBColor(0, 255, 0)
    BLUE = RGBColor(0, 0, 255)
    YELLOW = RGBColor(255, 255, 0)
    CYAN = RGBColor(0, 255, 255)
    MAGENTA = RGBColor(255, 0, 255)
    ORANGE = RGBColor(255, 165, 0)
    PURPLE = RGBColor(128, 0, 128)
    PINK = RGBColor(255, 192, 203)
    BROWN = RGBColor(165, 42, 42)
    GRAY = RGBColor(128, 128, 128)
    DARK_GRAY = RGBColor(64, 64, 64)
    LIGHT_GRAY = RGBColor(192, 192, 192)
    WARM_WHITE = RGBColor(255, 230, 180)
    COOL_WHITE = RGBColor(200, 220, 255)
    SOFT_WHITE = RGBColor(255, 245, 220)
    GAMING_RED = RGBColor(220, 20, 60)
    GAMING_BLUE = RGBColor(30, 144, 255)
    GAMING_GREEN = RGBColor(50, 205, 50)
    GAMING_PURPLE = RGBColor(138, 43, 226)

    @classmethod
    def get_all_colors(cls) -> Dict[str, RGBColor]:
        colors = {}
        for name in dir(cls):
            if not name.startswith('_') and name != 'get_all_colors':
                value = getattr(cls, name)
                if isinstance(value, RGBColor):
                    colors[name] = value
        return colors

    @classmethod
    def get_color_by_name(cls, name: str) -> Optional[RGBColor]:
        name = name.upper()
        return getattr(cls, name, None)

def create_rainbow_gradient(steps: int, saturation: float=1.0, value: float=1.0) -> List[RGBColor]:
    """create_rainbow_gradient method"""
    colors = []
    for i in range(steps):
        hue = i / steps * 360
        color = RGBColor.from_hsv(hue, saturation, value)
        colors.append(color)
    return colors

def parse_color_string(color_str: str) -> RGBColor:
    """parse_color_string method"""
    color_str = color_str.strip()
    if color_str.startswith('#') or RGBColor.HEX_PATTERN.match(color_str):
        return RGBColor.from_hex(color_str)
    predefined = Colors.get_color_by_name(color_str)
    if predefined:
        return predefined
    rgb_match = re.match('(?:rgb)?\\s*\\(\\s*(\\d+)\\s*,\\s*(\\d+)\\s*,\\s*(\\d+)\\s*\\)', color_str, re.IGNORECASE)
    if rgb_match:
        r, g, b = map(int, rgb_match.groups())
        return RGBColor(r, g, b)
    raise ValueError(f'Cannot parse color string: {color_str}')

def validate_color_list(colors: List[Any]) -> List[RGBColor]:
    """validate_color_list method"""
    validated_colors = []
    for i, color in enumerate(colors):
        try:
            if isinstance(color, RGBColor):
                validated_colors.append(color)
            elif isinstance(color, str):
                validated_colors.append(parse_color_string(color))
            elif isinstance(color, (tuple, list)) and len(color) == 3:
                validated_colors.append(RGBColor(*color))
            elif isinstance(color, dict):
                validated_colors.append(RGBColor(**color))
            else:
                raise ValueError(f'Invalid color format at index {i}')
        except Exception as e:
            raise ValueError(f'Error validating color at index {i}: {e}')
    return validated_colors

def get_optimal_osiris_brightness(rgb_colors: List[RGBColor], method: str='weighted_average') -> int:
    """get_optimal_osiris_brightness method"""
    if not rgb_colors:
        return 0
    brightnesses = [color.to_osiris_brightness() for color in rgb_colors]
    if method == 'max':
        return max(brightnesses)
    elif method == 'average':
        return int(sum(brightnesses) / len(brightnesses))
    else:
        total_weight = 0
        weighted_brightness = 0
        for brightness in brightnesses:
            weight = max(1, brightness)
            weighted_brightness += brightness * weight
            total_weight += weight
        return int(weighted_brightness / total_weight) if total_weight > 0 else 0