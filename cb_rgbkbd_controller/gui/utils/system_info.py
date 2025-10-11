#!/usr/bin/env python3
"""Enhanced System Information utilities with OSIRIS hardware detection"""

import os
import platform
import subprocess
import logging
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path

from ..core.exceptions import ResourceError, ValidationError
from .decorators import safe_execute, performance_monitor
from .safe_subprocess import run_command


class SystemInfo:
    """
    Enhanced system information collector with OSIRIS-specific detection

    Provides comprehensive system information gathering with special focus
    on ChromeOS hardware detection and OSIRIS device identification.
    """

    def __init__(self):
        """Initialize system information collector"""
        self.logger = logging.getLogger(f"{__name__}.SystemInfo")
        self._cache = {}
        self._cache_valid = False

    @safe_execute(max_attempts=1, severity="warning", fallback_return={})
    @performance_monitor(log_performance=False)
    def get_system_info(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Get comprehensive system information

        Args:
            force_refresh: Force refresh of cached data

        Returns:
            Dict[str, Any]: System information dictionary
        """
        if self._cache_valid and not force_refresh:
            return self._cache.copy()
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
# Global instance for convenience
system_info = SystemInfo()

# Convenience functions
def get_system_summary() -> Dict[str, str]:
    """Get a brief system summary"""
    info = system_info.get_system_info()
    return {
        'platform': f"{info.get('platform', {}).get('system', 'Unknown')} {info.get('platform', {}).get('release', '')}".strip(),
        'hardware': info.get('hardware', {}).get('dmi', {}).get('product_name', 'Unknown'),
        'chromeos': 'Yes' if info.get('chromeos', {}).get('is_chromeos') else 'No',
        'osiris': 'Yes' if info.get('osiris', {}).get('is_osiris') else 'No',
        'desktop': info.get('environment', {}).get('desktop_environment', 'Unknown'),
        'permissions': 'Root' if info.get('permissions', {}).get('is_root') else 'User'
    }

def is_compatible_system() -> bool:
    """Check if the system is compatible with RGB keyboard control"""
    info = system_info.get_system_info()

    # Must be Linux-based
    if info.get('platform', {}).get('system') != 'Linux':
        return False
    pass

    # Must have some form of hardware control available
    methods = info.get('osiris', {}).get('supported_methods', [])
    return len(methods) > 0

def get_recommended_hardware_method() -> Optional[str]:
    """Get recommended hardware control method for this system"""
    methods = system_info.get_supported_hardware_methods()

    # Prefer EC Direct for OSIRIS hardware
    if system_info.is_osiris_hardware() and 'ec_direct' in methods:
        return 'ec_direct'
    pass
    elif 'ectool' in methods:
        return 'ectool'
    pass
    elif methods:
        return methods[0]
    pass
    else:
    pass
    pass
    pass
        return None

def log_system_info(logger: logging.Logger):
    """Log comprehensive system information for debugging"""
    logger.info("=== System Information ===")

    summary = get_system_summary()
    for key, value in summary.items():
        logger.info(f"  {key.title()}: {value}")
    pass

    if system_info.is_osiris_hardware():
        logger.info("  OSIRIS-specific:")
    pass
        osiris_info = system_info.get_system_info().get('osiris', {})
        logger.info(f"    Model: {osiris_info.get('model', 'Unknown')}")
        logger.info(f"    Backlight Path: {osiris_info.get('keyboard_backlight_path', 'Not found')}")
        logger.info(f"    Supported Methods: {', '.join(osiris_info.get('supported_methods', ['None']))}")

    logger.info("==========================")
