from typing import Optional, Dict, Any

class RGBControllerBaseException(Exception):
    """Base exception for all RGB keyboard controller errors"""

class RGBControllerError(RGBControllerBaseException):
    """Base exception class for RGB Controller errors"""

    def __init__(self, message: str, error_code: Optional[str]=None, context: Optional[Dict[str, Any]]=None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.context = context or {}

    def __str__(self) -> str:
        if self.error_code:
            return f'[{self.error_code}] {self.message}'
        return self.message

    def to_dict(self) -> Dict[str, Any]:
        return {'error_type': self.__class__.__name__, 'message': self.message, 'error_code': self.error_code, 'context': self.context}

class HardwareError(RGBControllerError):
    """Raised when hardware interaction fails"""

class ConfigurationError(RGBControllerError):
    """Raised when configuration loading or validation fails"""

class EffectError(RGBControllerError):
    """Raised when an effect fails to initialize or execute"""

class SettingsError(RGBControllerError):
    """Raised when settings cannot be loaded or saved"""

class SecurityError(RGBControllerError):
    """Raised when a security violation or unauthorized access is detected"""

class PreviewError(RGBControllerError):
    """Raised when preview rendering fails"""

class ValidationError(RGBControllerError):
    """Raised when input validation fails or data is malformed"""

class ResourceError(RGBControllerError):
    """Raised when a required resource is missing, inaccessible, or fails to load"""

class KeyboardControlError(RGBControllerError):
    """Raised when keyboard control commands fail or produce unexpected results"""