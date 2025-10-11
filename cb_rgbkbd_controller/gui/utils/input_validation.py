#!/usr/bin/env python3
"""Enhanced Input Validation utilities for RGB Controller with OSIRIS optimization"""

import re
import json
from typing import Any, Union, List, Dict, Optional, Tuple
from pathlib import Path

from ..core.rgb_color import RGBColor, Colors, parse_color_string
from ..core.exceptions import ValidationError, ColorError


class SafeInputValidation:
    """
    Comprehensive input validation with enhanced security and type checking

    Provides validation methods for all types of user input in the RGB Controller,
    with special attention to OSIRIS hardware constraints and security considerations.
    """

    # Validation patterns
    HEX_COLOR_PATTERN = re.compile(r'^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    FILENAME_PATTERN = re.compile(r'^[a-zA-Z0-9._-]+$')
    SETTING_KEY_PATTERN = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]*$')

    # Safe ranges
    BRIGHTNESS_RANGE = (0, 100)
    SPEED_RANGE = (1, 10)
    ZONE_COUNT_RANGE = (1, 16)

    # Maximum string lengths to prevent DoS
    MAX_STRING_LENGTH = 1000
    MAX_FILENAME_LENGTH = 255
    MAX_JSON_SIZE = 10 * 1024 * 1024  # 10MB

    @classmethod
    def validate_integer(cls, value: Any, min_val: int = None, max_val: int = None,
        default: Optional[int] = None) -> Optional[int]:
        """
        Validate and convert value to integer within specified range

        Args:
            value: Value to validate
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            default: Default value if validation fails

        Returns:
            Optional[int]: Validated integer or default

        Raises:
            ValidationError: If validation fails and no default provided
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
# Convenience validation functions with safe defaults
def validate_brightness_safe(value: Any) -> int:
    """Safe brightness validation with default fallback (100%)"""
    return SafeInputValidation.validate_brightness(value, default=100)


def validate_color_safe(value: Any) -> RGBColor:
    """Safe color validation with default fallback (white)"""
    return SafeInputValidation.validate_color(value, default=RGBColor(255, 255, 255))


def validate_string_safe(value: Any, max_length: int = 1000) -> str:
    """Safe string validation with default fallback (empty string)"""
    return SafeInputValidation.validate_string(value, max_length=max_length, default="")


def validate_integer_safe(value: Any, min_val: int = None, max_val: int = None, fallback: int = 0) -> int:
    """Safe integer validation with fallback"""
    return SafeInputValidation.validate_integer(value, min_val, max_val, default=fallback)


def validate_filename_safe(value: Any) -> str:
    """Safe filename validation with timestamp fallback"""
    import time
    fallback_name = f"untitled_{int(time.time())}"
    return SafeInputValidation.validate_filename(value, default=fallback_name)


def validate_json_safe(value: Any) -> Dict[str, Any]:
    """Safe JSON validation with empty dict fallback"""
    return SafeInputValidation.validate_json_data(value, default={})


def validate_color_list_safe(colors: Any, min_count: int = 1) -> List[RGBColor]:
    """Safe color list validation with white color fallback"""
    fallback_colors = [RGBColor(255, 255, 255)] * min_count
    return SafeInputValidation.validate_color_list(colors, min_count=min_count, default=fallback_colors)


def sanitize_for_logging(value: Any, max_length: int = 200) -> str:
    """Sanitize value for safe logging"""
    return SafeInputValidation.sanitize_input_for_display(value, max_length)


def is_valid_hex_color(color_str: str) -> bool:
    """Quick check if string is valid hex color"""
    try:
    pass
    pass
    pass
    pass
except:
    pass
def is_valid_brightness(value: Any) -> bool:
    """Quick check if value is valid brightness"""
    try:
    pass
    pass
    pass
    pass
except:
    pass
def is_safe_filename(filename: str) -> bool:
    """Quick check if filename is safe"""
    try:
    pass
    pass
    pass
    pass
except:
    pass
# OSIRIS-specific validation shortcuts
def validate_osiris_brightness_conversion(colors: List[Any]) -> int:
    """Convert multiple colors to OSIRIS-optimal brightness"""
    return SafeInputValidation.validate_osiris_specific("brightness_conversion", colors)


def validate_osiris_zone_colors(colors: List[Any]) -> List[RGBColor]:
    """Validate zone colors for OSIRIS single-zone hardware"""
    return SafeInputValidation.validate_osiris_specific("zone_colors", colors)


# Security validation helpers
def validate_user_input_secure(value: Any, input_type: str = "string", **kwargs) -> Any:
    """
    Secure validation dispatcher for user inputs

    Args:
        value: Value to validate
        input_type: Type of input expected
        **kwargs: Additional validation parameters

    Returns:
        Any: Validated value with security checks applied
    """
    if input_type == "string":
        return SafeInputValidation.validate_string(value, **kwargs)
    pass
    elif input_type == "integer":
        return SafeInputValidation.validate_integer(value, **kwargs)
    pass
    elif input_type == "float":
        return SafeInputValidation.validate_float(value, **kwargs)
    pass
    elif input_type == "color":
        return SafeInputValidation.validate_color(value, **kwargs)
    pass
    elif input_type == "filename":
        return SafeInputValidation.validate_filename(value, **kwargs)
    pass
    elif input_type == "json":
        return SafeInputValidation.validate_json_data(value, **kwargs)
    pass
    elif input_type == "path":
        return SafeInputValidation.validate_path(value, **kwargs)
    pass
    else:
    pass
    pass
    pass
        raise ValidationError(f"Unknown input type for validation: {input_type}")


# Export all validation utilities
__all__ = [
    'SafeInputValidation',
    'validate_brightness_safe',
    'validate_color_safe',
    'validate_string_safe',
    'validate_integer_safe',
    'validate_filename_safe',
    'validate_json_safe',
    'validate_color_list_safe',
    'sanitize_for_logging',
    'is_valid_hex_color',
    'is_valid_brightness',
    'is_safe_filename',
    'validate_osiris_brightness_conversion',
    'validate_osiris_zone_colors',
    'validate_user_input_secure'
]
