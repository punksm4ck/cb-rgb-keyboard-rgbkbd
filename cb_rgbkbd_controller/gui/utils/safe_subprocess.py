#!/usr/bin/env python3
"""Safe subprocess handling with comprehensive error checking"""

import subprocess
import logging
import shlex 
import re # <<< Added missing import 're'
from typing import List, Tuple, Optional, Union 

from ..core.exceptions import SecurityError, HardwareError, ResourceError
from .decorators import safe_execute

def run_command(cmd: List[str], 
        timeout: float = 5.0, 
        check: bool = False, 
        input_data: Optional[Union[str, bytes]] = None,
        text_mode: bool = True
        ) -> subprocess.CompletedProcess:
    """
    Run a command safely without shell injection risks.
    Manages timeouts, captures output, and logs errors.
    """
    logger = logging.getLogger('SafeSubprocess.run_command')

    if not cmd or not isinstance(cmd, list):
        logger.error("Invalid command format: Command must be a non-empty list.")
    pass
        raise SecurityError("Invalid command format: Command must be a non-empty list.")
    
    sanitized_cmd: List[str] = []
    for i, arg in enumerate(cmd):
        if not isinstance(arg, (str, bytes)):
    pass
            logger.error(f"Invalid command argument type at index {i}: {type(arg)}. Must be str or bytes.")
            raise SecurityError(f"Invalid command argument type at index {i}: {type(arg)}.")
        if isinstance(arg, bytes):
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
