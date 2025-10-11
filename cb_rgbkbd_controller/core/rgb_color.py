#!/usr/bin/env python3
"""Enhanced RGB Color class with OSIRIS optimization and comprehensive validation"""

import re
import colorsys
import math
from typing import Union, Tuple, Dict, Any, Optional, List
import json


class RGBColor:
    """
    Enhanced RGB Color class with OSIRIS hardware optimization and comprehensive validation

    Supports multiple color formats, validation, conversion utilities, and OSIRIS-specific
    brightness calculation for single-zone white backlight hardware.
    """

    # Color validation constants
    MIN_VALUE = 0
    MAX_VALUE = 255
    HEX_PATTERN = re.compile(r'^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')

    # OSIRIS luminance coefficients (ITU-R BT.709 standard)
    LUMINANCE_RED = 0.2126
    LUMINANCE_GREEN = 0.7152
    LUMINANCE_BLUE = 0.0722

    # Alternative luminance coefficients (NTSC standard - more perceptual)
    NTSC_LUMINANCE_RED = 0.299
    NTSC_LUMINANCE_GREEN = 0.587
    NTSC_LUMINANCE_BLUE = 0.114

    def __init__(self, r: int = 0, g: int = 0, b: int = 0):
        """
        Initialize RGB color with validation

        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)

        Raises:
            ValueError: If color values are invalid
        """
        self._r = self._validate_component(r, "red")
        self._g = self._validate_component(g, "green")
        self._b = self._validate_component(b, "blue")

    @property
    def r(self) -> int:
        """Red component (0-255)"""
        return self._r

    @r.setter
    def r(self, value: int):
        """Set red component with validation"""
        self._r = self._validate_component(value, "red")

    @property
    def g(self) -> int:
        """Green component (0-255)"""
        return self._g

    @g.setter
    def g(self, value: int):
        """Set green component with validation"""
        self._g = self._validate_component(value, "green")

    @property
    def b(self) -> int:
        """Blue component (0-255)"""
        return self._b

    @b.setter
    def b(self, value: int):
        """Set blue component with validation"""
        self._b = self._validate_component(value, "blue")

    def _validate_component(self, value: Union[int, float], component_name: str = "component") -> int:
        """
        Validate a single color component

        Args:
            value: Component value to validate
            component_name: Name of component for error messages

        Returns:
            int: Validated component value

        Raises:
            ValueError: If component value is invalid
        """
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
# Predefined color constants for convenience
class Colors:
    """Predefined RGB color constants"""

    # Basic colors
    BLACK = RGBColor(0, 0, 0)
    WHITE = RGBColor(255, 255, 255)
    RED = RGBColor(255, 0, 0)
    GREEN = RGBColor(0, 255, 0)
    BLUE = RGBColor(0, 0, 255)
    YELLOW = RGBColor(255, 255, 0)
    CYAN = RGBColor(0, 255, 255)
    MAGENTA = RGBColor(255, 0, 255)

    # Extended colors
    ORANGE = RGBColor(255, 165, 0)
    PURPLE = RGBColor(128, 0, 128)
    PINK = RGBColor(255, 192, 203)
    BROWN = RGBColor(165, 42, 42)
    GRAY = RGBColor(128, 128, 128)
    DARK_GRAY = RGBColor(64, 64, 64)
    LIGHT_GRAY = RGBColor(192, 192, 192)

    # Warm colors for OSIRIS (good for single-zone white backlight)
    WARM_WHITE = RGBColor(255, 230, 180)
    COOL_WHITE = RGBColor(200, 220, 255)
    SOFT_WHITE = RGBColor(255, 245, 220)

    # Popular gaming colors
    GAMING_RED = RGBColor(220, 20, 60)
    GAMING_BLUE = RGBColor(30, 144, 255)
    GAMING_GREEN = RGBColor(50, 205, 50)
    GAMING_PURPLE = RGBColor(138, 43, 226)

    @classmethod
    def get_all_colors(cls) -> Dict[str, RGBColor]:
        """Get all predefined colors as a dictionary"""
        colors = {}
        for name in dir(cls):
            if not name.startswith('_') and name != 'get_all_colors':
    pass
        value = getattr(cls, name)
        if isinstance(value, RGBColor):
        colors[name] = value
    pass
        return colors

    @classmethod
    def get_color_by_name(cls, name: str) -> Optional[RGBColor]:
        """Get a predefined color by name (case-insensitive)"""
        name = name.upper()
        return getattr(cls, name, None)


# Utility functions for color operations
def create_gradient(start_color: RGBColor, end_color: RGBColor, steps: int) -> List[RGBColor]:
    """
    Create a gradient between two colors

    Args:
        start_color: Starting color
        end_color: Ending color
        steps: Number of steps in gradient

    Returns:
        List[RGBColor]: Gradient colors
    """
    return RGBColor.interpolate(start_color, end_color, steps)


def create_rainbow_gradient(steps: int, saturation: float = 1.0, value: float = 1.0) -> List[RGBColor]:
    """
    Create a rainbow gradient

    Args:
        steps: Number of colors in rainbow
        saturation: Color saturation (0.0-1.0)
        value: Color brightness (0.0-1.0)

    Returns:
        List[RGBColor]: Rainbow colors
    """
    colors = []
    for i in range(steps):
        hue = (i / steps) * 360
    pass
        color = RGBColor.from_hsv(hue, saturation, value)
        colors.append(color)
    return colors


def parse_color_string(color_str: str) -> RGBColor:
    """
    Parse various color string formats

    Args:
        color_str: Color string (hex, name, rgb tuple as string)

    Returns:
        RGBColor: Parsed color

    Raises:
        ValueError: If color string cannot be parsed
    """
    color_str = color_str.strip()

    # Try hex format first
    if color_str.startswith('#') or all(c in '0123456789ABCDEFabcdef' for c in color_str):
        return RGBColor.from_hex(color_str)
    pass

    # Try predefined color name
    predefined = Colors.get_color_by_name(color_str)
    if predefined:
        return predefined
    pass

    # Try RGB tuple format: "rgb(255,0,0)" or "(255,0,0)"
    rgb_match = re.match(r'(?:rgb)?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', color_str, re.IGNORECASE)
    if rgb_match:
        r, g, b = map(int, rgb_match.groups())
    pass
        return RGBColor(r, g, b)

    raise ValueError(f"Cannot parse color string: {color_str}")


def validate_color_list(colors: List[Any]) -> List[RGBColor]:
    """
    Validate and convert a list of color representations to RGBColor objects

    Args:
        colors: List of color representations (hex, dict, tuple, RGBColor)

    Returns:
        List[RGBColor]: Validated color list

    Raises:
        ValueError: If any color is invalid
    """
    validated_colors = []

    for i, color in enumerate(colors):
        try:
    pass
    pass
    pass
    pass
except:
    pass
def get_optimal_osiris_brightness(rgb_colors: List[RGBColor], method: str = "weighted_average") -> int:
    """
    Calculate optimal brightness for OSIRIS hardware from multiple RGB colors

    Args:
        rgb_colors: List of RGB colors to convert
        method: Conversion method ("weighted_average", "max", "average")

    Returns:
        int: Optimal brightness level (0-100)
    """
    if not rgb_colors:
        return 0
    pass

    if method == "max":
        # Use the brightest color
    pass
        brightnesses = [color.to_osiris_brightness() for color in rgb_colors]
        return max(brightnesses)

    elif method == "average":
        # Simple average
    pass
        brightnesses = [color.to_osiris_brightness() for color in rgb_colors]
        return int(sum(brightnesses) / len(brightnesses))

    else:  # weighted_average (default)
        # Weight by perceived brightness
        total_weight = 0
        weighted_brightness = 0

        for color in rgb_colors:
            brightness = color.to_osiris_brightness()
    pass
            weight = max(1, brightness)  # Prevent zero weight
            weighted_brightness += brightness * weight
            total_weight += weight

        if total_weight > 0:
            return int(weighted_brightness / total_weight)
    pass
        else:
    pass
    pass
    pass
            return 0
