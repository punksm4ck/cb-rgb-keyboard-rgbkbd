#!/usr/bin/env python3
"""Enhanced Exceptions for RGB Controller with OSIRIS-specific error handling"""

from typing import Optional, Dict, Any


class RGBControllerError(Exception):
    """Base exception class for RGB Controller errors"""

    def __init__(self, message: str, error_code: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
        """
        Initialize RGB Controller error

        Args:
            message: Error message
            error_code: Optional error code for categorization
            context: Optional context information
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.context = context or {}

    def __str__(self) -> str:
        """String representation of error"""
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
    pass
        return self.message

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging/serialization"""
        return {
            'error_type': self.__class__.__name__,
            'message': self.message,
            'error_code': self.error_code,
            'context': self.context
        }


class HardwareError(RGBControllerError):
    """Hardware-related errors for RGB keyboard control"""

    def __init__(self, message: str, hardware_method: Optional[str] = None,
        device_info: Optional[Dict[str, Any]] = None, **kwargs):
        """
        Initialize hardware error

        Args:
            message: Error message
            hardware_method: Hardware control method that failed
            device_info: Device information context
            **kwargs: Additional context
        """
        context = kwargs.get('context', {})
        if hardware_method:
            context['hardware_method'] = hardware_method
    pass
        if device_info:
            context['device_info'] = device_info
    pass

        super().__init__(message, kwargs.get('error_code', 'HW_ERROR'), context)
        self.hardware_method = hardware_method
        self.device_info = device_info


class OSIRISHardwareError(HardwareError):
    """OSIRIS-specific hardware errors"""

    def __init__(self, message: str, osiris_operation: Optional[str] = None,
        sysfs_path: Optional[str] = None, **kwargs):
        """
        Initialize OSIRIS hardware error

        Args:
            message: Error message
            osiris_operation: Specific OSIRIS operation that failed
            sysfs_path: ChromeOS sysfs path involved
            **kwargs: Additional context
        """
        context = kwargs.get('context', {})
        context.update({
            'device_type': 'OSIRIS',
            'osiris_operation': osiris_operation,
            'sysfs_path': sysfs_path
        })

        super().__init__(message, 'ec_direct', {'device_type': 'OSIRIS'},
        error_code='OSIRIS_HW_ERROR', context=context)
        self.osiris_operation = osiris_operation
        self.sysfs_path = sysfs_path


class KeyboardControlError(HardwareError):
    """Keyboard control specific errors"""

    def __init__(self, message: str, operation: Optional[str] = None, **kwargs):
        """
        Initialize keyboard control error

        Args:
            message: Error message
            operation: Keyboard operation that failed
            **kwargs: Additional context
        """
        context = kwargs.get('context', {})
        if operation:
            context['operation'] = operation
    pass

        super().__init__(message, error_code='KB_CONTROL_ERROR', context=context)
        self.operation = operation


class ECToolError(HardwareError):
    """ectool-specific errors"""

    def __init__(self, message: str, ectool_command: Optional[str] = None,
        return_code: Optional[int] = None, stderr: Optional[str] = None, **kwargs):
        """
        Initialize ectool error

        Args:
            message: Error message
            ectool_command: ectool command that failed
            return_code: Process return code
            stderr: Standard error output
            **kwargs: Additional context
        """
        context = kwargs.get('context', {})
        context.update({
            'ectool_command': ectool_command,
            'return_code': return_code,
            'stderr': stderr
        })

        super().__init__(message, 'ectool', error_code='ECTOOL_ERROR', context=context)
        self.ectool_command = ectool_command
        self.return_code = return_code
        self.stderr = stderr


class PermissionError(HardwareError):
    """Permission-related errors for hardware access"""

    def __init__(self, message: str, required_permission: Optional[str] = None,
        suggested_solution: Optional[str] = None, **kwargs):
        """
        Initialize permission error

        Args:
            message: Error message
            required_permission: Required permission level
            suggested_solution: Suggested solution
            **kwargs: Additional context
        """
        context = kwargs.get('context', {})
        context.update({
            'required_permission': required_permission,
            'suggested_solution': suggested_solution
        })

        super().__init__(message, error_code='PERMISSION_ERROR', context=context)
        self.required_permission = required_permission
        self.suggested_solution = suggested_solution


class ConfigurationError(RGBControllerError):
    """Configuration and settings related errors"""

    def __init__(self, message: str, config_key: Optional[str] = None,
        config_value: Optional[Any] = None, **kwargs):
        """
        Initialize configuration error

        Args:
            message: Error message
            config_key: Configuration key that caused error
            config_value: Invalid configuration value
            **kwargs: Additional context
        """
        context = kwargs.get('context', {})
        context.update({
            'config_key': config_key,
            'config_value': str(config_value) if config_value is not None else None
        })

        super().__init__(message, error_code='CONFIG_ERROR', context=context)
        self.config_key = config_key
        self.config_value = config_value


class ValidationError(RGBControllerError):
    """Data validation errors"""

    def __init__(self, message: str, field_name: Optional[str] = None,
        invalid_value: Optional[Any] = None, expected_type: Optional[str] = None, **kwargs):
        """
        Initialize validation error

        Args:
            message: Error message
            field_name: Field that failed validation
            invalid_value: The invalid value
            expected_type: Expected data type or format
            **kwargs: Additional context
        """
        context = kwargs.get('context', {})
        context.update({
            'field_name': field_name,
            'invalid_value': str(invalid_value) if invalid_value is not None else None,
            'expected_type': expected_type
        })

        super().__init__(message, error_code='VALIDATION_ERROR', context=context)
        self.field_name = field_name
        self.invalid_value = invalid_value
        self.expected_type = expected_type


class ColorError(ValidationError):
    """Color validation and conversion errors"""

    def __init__(self, message: str, color_data: Optional[Any] = None,
        color_format: Optional[str] = None, **kwargs):
        """
        Initialize color error

        Args:
            message: Error message
            color_data: Invalid color data
            color_format: Expected color format
            **kwargs: Additional context
        """
        context = kwargs.get('context', {})
        context.update({
            'color_data': str(color_data) if color_data is not None else None,
            'color_format': color_format
        })

        super().__init__(message, field_name='color', invalid_value=color_data,
        expected_type=color_format, error_code='COLOR_ERROR', context=context)
        self.color_data = color_data
        self.color_format = color_format


class EffectError(RGBControllerError):
    """Effect-related errors"""

    def __init__(self, message: str, effect_name: Optional[str] = None,
        effect_parameter: Optional[str] = None, **kwargs):
        """
        Initialize effect error

        Args:
            message: Error message
            effect_name: Name of the effect that failed
            effect_parameter: Specific parameter that caused error
            **kwargs: Additional context
        """
        context = kwargs.get('context', {})
        context.update({
            'effect_name': effect_name,
            'effect_parameter': effect_parameter
        })

        super().__init__(message, error_code='EFFECT_ERROR', context=context)
        self.effect_name = effect_name
        self.effect_parameter = effect_parameter


class ResourceError(RGBControllerError):
    """Resource-related errors (memory, file access, etc.)"""

    def __init__(self, message: str, resource_type: Optional[str] = None,
        resource_path: Optional[str] = None, **kwargs):
        """
        Initialize resource error

        Args:
            message: Error message
            resource_type: Type of resource that failed
            resource_path: Path to the resource
            **kwargs: Additional context
        """
        context = kwargs.get('context', {})
        context.update({
            'resource_type': resource_type,
            'resource_path': resource_path
        })

        super().__init__(message, error_code='RESOURCE_ERROR', context=context)
        self.resource_type = resource_type
        self.resource_path = resource_path


class DependencyError(RGBControllerError):
    """Missing or incompatible dependency errors"""

    def __init__(self, message: str, dependency_name: Optional[str] = None,
        required_version: Optional[str] = None, current_version: Optional[str] = None, **kwargs):
        """
        Initialize dependency error

        Args:
            message: Error message
            dependency_name: Name of the missing dependency
            required_version: Required version
            current_version: Currently installed version
            **kwargs: Additional context
        """
        context = kwargs.get('context', {})
        context.update({
            'dependency_name': dependency_name,
            'required_version': required_version,
            'current_version': current_version
        })

        super().__init__(message, error_code='DEPENDENCY_ERROR', context=context)
        self.dependency_name = dependency_name
        self.required_version = required_version
        self.current_version = current_version


class TimeoutError(RGBControllerError):
    """Timeout-related errors"""

    def __init__(self, message: str, operation: Optional[str] = None,
        timeout_duration: Optional[float] = None, **kwargs):
        """
        Initialize timeout error

        Args:
            message: Error message
            operation: Operation that timed out
            timeout_duration: Timeout duration in seconds
            **kwargs: Additional context
        """
        context = kwargs.get('context', {})
        context.update({
            'operation': operation,
            'timeout_duration': timeout_duration
        })

        super().__init__(message, error_code='TIMEOUT_ERROR', context=context)
        self.operation = operation
        self.timeout_duration = timeout_duration


class CriticalError(RGBControllerError):
    """Critical errors that require application shutdown"""

    def __init__(self, message: str, recovery_possible: bool = False, **kwargs):
        """
        Initialize critical error

        Args:
            message: Error message
            recovery_possible: Whether recovery might be possible
            **kwargs: Additional context
        """
        context = kwargs.get('context', {})
        context['recovery_possible'] = recovery_possible

        super().__init__(message, error_code='CRITICAL_ERROR', context=context)
        self.recovery_possible = recovery_possible


# Utility functions for error handling
def format_error_for_user(error: Exception) -> str:
    """
    Format an error for user-friendly display

    Args:
        error: Exception to format

    Returns:
        str: User-friendly error message
    """
    if isinstance(error, OSIRISHardwareError):
        return f"OSIRIS Hardware Error: {error.message}\nOperation: {error.osiris_operation or 'Unknown'}"
    pass

    elif isinstance(error, ECToolError):
        return f"ectool Error: {error.message}\nCommand: {error.ectool_command or 'Unknown'}"
    pass

    elif isinstance(error, PermissionError):
        msg = f"Permission Error: {error.message}"
    pass
        if error.suggested_solution:
            msg += f"\nSuggested Solution: {error.suggested_solution}"
    pass
        return msg

    elif isinstance(error, DependencyError):
        msg = f"Dependency Error: {error.message}"
    pass
        if error.dependency_name:
            msg += f"\nMissing: {error.dependency_name}"
    pass
        if error.required_version:
            msg += f"\nRequired Version: {error.required_version}"
    pass
        return msg

    elif isinstance(error, ColorError):
        return f"Color Error: {error.message}\nInvalid Color: {error.color_data}"
    pass

    elif isinstance(error, RGBControllerError):
        return f"{error.__class__.__name__}: {error.message}"
    pass

    else:
    pass
    pass
    pass
        return f"Unexpected Error: {str(error)}"


def get_error_category(error: Exception) -> str:
    """
    Get error category for logging and handling

    Args:
        error: Exception to categorize

    Returns:
        str: Error category
    """
    if isinstance(error, (HardwareError, OSIRISHardwareError, ECToolError)):
        return "hardware"
    pass
    elif isinstance(error, (ConfigurationError, ValidationError, ColorError)):
        return "configuration"
    pass
    elif isinstance(error, PermissionError):
        return "permissions"
    pass
    elif isinstance(error, DependencyError):
        return "dependencies"
    pass
    elif isinstance(error, EffectError):
        return "effects"
    pass
    elif isinstance(error, ResourceError):
        return "resources"
    pass
    elif isinstance(error, TimeoutError):
        return "timeout"
    pass
    elif isinstance(error, CriticalError):
        return "critical"
    pass
    else:
    pass
    pass
    pass
        return "general"


def should_retry_operation(error: Exception, retry_count: int = 0, max_retries: int = 3) -> bool:
    """
    Determine if an operation should be retried based on the error type

    Args:
        error: Exception that occurred
        retry_count: Current retry count
        max_retries: Maximum number of retries

    Returns:
        bool: True if operation should be retried
    """
    if retry_count >= max_retries:
        return False
    pass

    # Don't retry certain error types
    if isinstance(error, (ValidationError, ColorError, ConfigurationError, DependencyError, CriticalError)):
        return False
    pass

    # Retry hardware errors and timeouts
    if isinstance(error, (HardwareError, TimeoutError, ResourceError)):
        return True
    pass

    # Don't retry permission errors (they won't fix themselves)
    if isinstance(error, PermissionError):
        return False
    pass

    # Default to not retrying unknown errors
    return False


def log_error_context(logger, error: Exception, operation: Optional[str] = None):
    """
    Log error with full context information

    Args:
        logger: Logger instance
        error: Exception to log
        operation: Optional operation context
    """
    error_info = {
        'error_type': type(error).__name__,
        'message': str(error),
        'operation': operation,
        'category': get_error_category(error)
    }

    if isinstance(error, RGBControllerError):
        error_info.update(error.to_dict())
    pass

    logger.error(f"Operation failed: {operation or 'Unknown'}", extra=error_info)

    # Log additional context for specific error types
    if isinstance(error, HardwareError):
        logger.error(f"Hardware method: {getattr(error, 'hardware_method', 'Unknown')}")
    pass

    if isinstance(error, ECToolError):
        logger.error(f"ectool command: {getattr(error, 'ectool_command', 'Unknown')}")
    pass
        logger.error(f"Return code: {getattr(error, 'return_code', 'Unknown')}")
