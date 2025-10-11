#!/usr/bin/env python3
"""Complete Effects Library for RGB Controller with OSIRIS per-key optimization"""

import math
import time
import random
import threading
from typing import List, Dict, Any, Optional, Callable, Tuple
import colorsys

from ..core.rgb_color import RGBColor, Colors, create_rainbow_gradient
from ..core.exceptions import EffectError
from ..core.constants import TOTAL_LEDS, NUM_ZONES, ANIMATION_FRAME_DELAY
from ..utils.decorators import safe_execute, performance_monitor

# Hardware mapping for OSIRIS - 100 individual keys
OSIRIS_KEY_COUNT = 100
OSIRIS_KEY_LAYOUT = {
    # Row 1 - Function keys
    'F1': 0, 'F2': 1, 'F3': 2, 'F4': 3, 'F5': 4, 'F6': 5, 'F7': 6, 'F8': 7, 'F9': 8, 'F10': 9,

    # Row 2 - Number row
    '`': 10, '1': 11, '2': 12, '3': 13, '4': 14, '5': 15, '6': 16, '7': 17, '8': 18, '9': 19, '0': 20,
    '-': 21, '=': 22, 'Backspace': 23,

    # Row 3 - QWERTY row
    'Tab': 24, 'Q': 25, 'W': 26, 'E': 27, 'R': 28, 'T': 29, 'Y': 30, 'U': 31, 'I': 32, 'O': 33,
    'P': 34, '[': 35, ']': 36, '\\': 37,

    # Row 4 - ASDF row
    'CapsLock': 38, 'A': 39, 'S': 40, 'D': 41, 'F': 42, 'G': 43, 'H': 44, 'J': 45, 'K': 46, 'L': 47,
    ';': 48, "'": 49, 'Enter': 50,

    # Row 5 - ZXCV row
    'LShift': 51, 'Z': 52, 'X': 53, 'C': 54, 'V': 55, 'B': 56, 'N': 57, 'M': 58, ',': 59, '.': 60,
    '/': 61, 'RShift': 62,

    # Row 6 - Bottom row
    'LCtrl': 63, 'Fn': 64, 'LAlt': 65, 'Space': 66, 'RAlt': 67, 'RCtrl': 68,

    # Arrow cluster and additional keys
    'Up': 69, 'Down': 70, 'Left': 71, 'Right': 72,

    # Additional keys to reach 100 total
    'Home': 73, 'End': 74, 'PageUp': 75, 'PageDown': 76, 'Insert': 77, 'Delete': 78,
    'PrintScreen': 79, 'ScrollLock': 80, 'Pause': 81,

    # Extra zones for full coverage
    **{f'Extra{i}': 82 + i for i in range(18)}  # Extra0-Extra17 = zones 82-99
}

# Reverse mapping for position-based effects
KEY_POSITIONS = {v: k for k, v in OSIRIS_KEY_LAYOUT.items()}


class BaseEffect:
    """Base class for all lighting effects"""

    def __init__(self, name: str, speed: int = 5, color: RGBColor = None, **params):
        """
        Initialize base effect

        Args:
            name: Effect name
            speed: Effect speed (1-10)
            color: Primary effect color
            **params: Additional effect parameters
        """
        self.name = name
        self.speed = max(1, min(10, speed))
        self.color = color or Colors.WHITE
        self.params = params
        self.is_running = False
        self.frame_count = 0
        self.start_time = 0.0
        self._lock = threading.Lock()

    def get_frame_delay(self) -> float:
        """Calculate frame delay based on speed (1=slowest, 10=fastest)"""
        return ANIMATION_FRAME_DELAY * (11 - self.speed) / 10

    def start(self):
        """Start the effect"""
        with self._lock:
            self.is_running = True
    pass
            self.frame_count = 0
            self.start_time = time.time()

    def stop(self):
        """Stop the effect"""
        with self._lock:
            self.is_running = False
    pass

    def get_colors(self) -> List[RGBColor]:
        """
        Get current frame colors for all keys

        Returns:
            List[RGBColor]: Colors for all 100 keys
        """
        raise NotImplementedError("Subclasses must implement get_colors()")

    def advance_frame(self):
        """Advance to next animation frame"""
        with self._lock:
            if self.is_running:
    pass
        self.frame_count += 1


class StaticColorEffect(BaseEffect):
    """Static single color across all keys"""

    def __init__(self, color: RGBColor = Colors.WHITE, **params):
        super().__init__("Static Color", color=color, **params)

    def get_colors(self) -> List[RGBColor]:
        return [self.color] * OSIRIS_KEY_COUNT


class ColorShiftEffect(BaseEffect):
    """Smooth transition between colors over time"""

    def __init__(self, start_color: RGBColor = Colors.RED, end_color: RGBColor = Colors.BLUE,
        speed: int = 5, **params):
        super().__init__("Color Shift", speed=speed, **params)
        self.start_color = start_color
        self.end_color = end_color

    def get_colors(self) -> List[RGBColor]:
        if not self.is_running:
            return [Colors.BLACK] * OSIRIS_KEY_COUNT
    pass

        # Calculate blend ratio based on time and speed
        elapsed = time.time() - self.start_time
        cycle_duration = 5.0 / self.speed  # Faster speed = shorter cycles
        progress = (elapsed % cycle_duration) / cycle_duration

        # Smooth transition using sine wave
        blend_ratio = (math.sin(progress * 2 * math.pi) + 1) / 2

        current_color = self.start_color.blend_with(self.end_color, blend_ratio)
        return [current_color] * OSIRIS_KEY_COUNT


class RainbowWaveEffect(BaseEffect):
    """Flowing rainbow effect across the keyboard"""

    def __init__(self, speed: int = 5, direction: str = "horizontal", **params):
        super().__init__("Rainbow Wave", speed=speed, **params)
        self.direction = direction  # horizontal, vertical, diagonal

    def get_colors(self) -> List[RGBColor]:
        if not self.is_running:
            return [Colors.BLACK] * OSIRIS_KEY_COUNT
    pass

        colors = []
        elapsed = time.time() - self.start_time
        wave_speed = self.speed * 2

        for key_id in range(OSIRIS_KEY_COUNT):
            if self.direction == "horizontal":
    pass
        position = (key_id % 14) / 14.0  # 14 keys per row approximate
            elif self.direction == "vertical":
        position = (key_id // 14) / 7.0  # 7 rows approximate
    pass
            else:  # diagonal
        row = key_id // 14
        col = key_id % 14
        position = (row + col) / 20.0

            # Create moving rainbow wave
            hue = ((position * 360 + elapsed * wave_speed * 60) % 360)
            color = RGBColor.from_hsv(hue, 1.0, 1.0)
            colors.append(color)

        return colors


class BreathingEffect(BaseEffect):
    """Keys fade in and out like breathing"""

    def __init__(self, color: RGBColor = Colors.WHITE, speed: int = 5, **params):
        super().__init__("Breathing", speed=speed, color=color, **params)

    def get_colors(self) -> List[RGBColor]:
        if not self.is_running:
            return [Colors.BLACK] * OSIRIS_KEY_COUNT
    pass

        elapsed = time.time() - self.start_time
        breath_rate = self.speed / 5.0  # Normalize speed

        # Sine wave for smooth breathing
        intensity = (math.sin(elapsed * breath_rate * math.pi) + 1) / 2
        breathing_color = self.color * intensity

        return [breathing_color] * OSIRIS_KEY_COUNT


class ReactiveKeypressEffect(BaseEffect):
    """Keys light up when pressed"""

    def __init__(self, color: RGBColor = Colors.WHITE, fade_time: float = 1.0, **params):
        super().__init__("Reactive Keypress", color=color, **params)
        self.fade_time = fade_time
        self.active_keys: Dict[int, float] = {}  # key_id: press_time

    def trigger_key(self, key_id: int):
        """Trigger reactive effect for specific key"""
        if 0 <= key_id < OSIRIS_KEY_COUNT:
            self.active_keys[key_id] = time.time()
    pass

    def get_colors(self) -> List[RGBColor]:
        colors = [Colors.BLACK] * OSIRIS_KEY_COUNT
        current_time = time.time()

        # Remove expired keys
        expired_keys = [k for k, t in self.active_keys.items()
        if current_time - t > self.fade_time]
        for k in expired_keys:
            del self.active_keys[k]
    pass

        # Apply colors to active keys
        for key_id, press_time in self.active_keys.items():
            elapsed = current_time - press_time
    pass
            intensity = max(0, 1 - (elapsed / self.fade_time))
            colors[key_id] = self.color * intensity

        return colors


class RippleEffect(BaseEffect):
    """Light radiates outward from pressed keys"""

    def __init__(self, color: RGBColor = Colors.CYAN, ripple_speed: float = 20.0, **params):
        super().__init__("Ripple", color=color, **params)
        self.ripple_speed = ripple_speed
        self.ripples: List[Dict[str, Any]] = []  # List of active ripples

    def trigger_ripple(self, center_key: int):
        """Start ripple effect from center key"""
        if 0 <= center_key < OSIRIS_KEY_COUNT:
            self.ripples.append({
    pass
        'center': center_key,
        'start_time': time.time(),
        'max_radius': 15.0  # Maximum ripple radius
            })

    def _get_key_position(self, key_id: int) -> Tuple[float, float]:
        """Get approximate X,Y position of key for distance calculation"""
        row = key_id // 14
        col = key_id % 14
        return (col, row)

    def get_colors(self) -> List[RGBColor]:
        colors = [Colors.BLACK] * OSIRIS_KEY_COUNT
        current_time = time.time()

        # Remove expired ripples
        self.ripples = [r for r in self.ripples
        if current_time - r['start_time'] < r['max_radius'] / self.ripple_speed]

        # Apply ripple effects
        for ripple in self.ripples:
            elapsed = current_time - ripple['start_time']
    pass
            current_radius = elapsed * self.ripple_speed

            center_pos = self._get_key_position(ripple['center'])

            for key_id in range(OSIRIS_KEY_COUNT):
        key_pos = self._get_key_position(key_id)
    pass
        distance = math.sqrt((key_pos[0] - center_pos[0])**2 +
        (key_pos[1] - center_pos[1])**2)

        # Create ripple wave
        if abs(distance - current_radius) < 2.0:  # Wave thickness
        intensity = max(0, 1 - abs(distance - current_radius) / 2.0)
        ripple_color = self.color * intensity
        colors[key_id] = colors[key_id] + ripple_color

        return colors


class PulseWaveEffect(BaseEffect):
    """Expanding rings of light from center"""

    def __init__(self, color: RGBColor = Colors.PURPLE, speed: int = 5, **params):
        super().__init__("Pulse Wave", speed=speed, color=color, **params)
        self.center_key = OSIRIS_KEY_COUNT // 2  # Center of keyboard

    def get_colors(self) -> List[RGBColor]:
        if not self.is_running:
            return [Colors.BLACK] * OSIRIS_KEY_COUNT
    pass

        colors = [Colors.BLACK] * OSIRIS_KEY_COUNT
        elapsed = time.time() - self.start_time
        wave_speed = self.speed * 5

        center_pos = self._get_key_position(self.center_key)
        current_radius = (elapsed * wave_speed) % 20  # Wave repeats

        for key_id in range(OSIRIS_KEY_COUNT):
            key_pos = self._get_key_position(key_id)
    pass
            distance = math.sqrt((key_pos[0] - center_pos[0])**2 +
        (key_pos[1] - center_pos[1])**2)

            # Create expanding wave
            wave_thickness = 3.0
            if abs(distance - current_radius) < wave_thickness:
        intensity = 1 - abs(distance - current_radius) / wave_thickness
    pass
        colors[key_id] = self.color * intensity

        return colors

    def _get_key_position(self, key_id: int) -> Tuple[float, float]:
        """Get approximate X,Y position of key"""
        row = key_id // 14
        col = key_id % 14
        return (col, row)


class ScanningBeamEffect(BaseEffect):
    """Light bar sweeps across keyboard"""

    def __init__(self, color: RGBColor = Colors.RED, speed: int = 5, direction: str = "horizontal", **params):
        super().__init__("Scanning Beam", speed=speed, color=color, **params)
        self.direction = direction

    def get_colors(self) -> List[RGBColor]:
        if not self.is_running:
            return [Colors.BLACK] * OSIRIS_KEY_COUNT
    pass

        colors = [Colors.BLACK] * OSIRIS_KEY_COUNT
        elapsed = time.time() - self.start_time
        scan_speed = self.speed * 2

        if self.direction == "horizontal":
            rows = 7  # Approximate keyboard rows
    pass
            current_row = int((elapsed * scan_speed) % rows)

            for key_id in range(OSIRIS_KEY_COUNT):
        key_row = key_id // 14
    pass
        if key_row == current_row:
        colors[key_id] = self.color
    pass

        else:  # vertical
            cols = 14  # Approximate keyboard columns
            current_col = int((elapsed * scan_speed) % cols)

            for key_id in range(OSIRIS_KEY_COUNT):
        key_col = key_id % 14
    pass
        if key_col == current_col:
        colors[key_id] = self.color
    pass

        return colors


class SnakeEffect(BaseEffect):
    """Moving snake of light across keyboard"""

    def __init__(self, color: RGBColor = Colors.GREEN, speed: int = 5, length: int = 8, **params):
        super().__init__("Snake", speed=speed, color=color, **params)
        self.length = length
        self.path = list(range(OSIRIS_KEY_COUNT))  # Snake path
        random.shuffle(self.path)  # Randomize path

    def get_colors(self) -> List[RGBColor]:
        if not self.is_running:
            return [Colors.BLACK] * OSIRIS_KEY_COUNT
    pass

        colors = [Colors.BLACK] * OSIRIS_KEY_COUNT
        elapsed = time.time() - self.start_time
        move_speed = self.speed * 3

        head_position = int(elapsed * move_speed) % len(self.path)

        # Draw snake body
        for i in range(self.length):
            pos = (head_position - i) % len(self.path)
    pass
            key_id = self.path[pos]

            # Fade from head to tail
            intensity = (self.length - i) / self.length
            colors[key_id] = self.color * intensity

        return colors


class MeteorEffect(BaseEffect):
    """Fast-moving streaks with trailing fade"""

    def __init__(self, color: RGBColor = Colors.YELLOW, speed: int = 8, trail_length: int = 12, **params):
        super().__init__("Meteor", speed=speed, color=color, **params)
        self.trail_length = trail_length
        self.meteors: List[Dict[str, Any]] = []

    def get_colors(self) -> List[RGBColor]:
        colors = [Colors.BLACK] * OSIRIS_KEY_COUNT
        current_time = time.time()

        # Spawn new meteors randomly
        if random.random() < 0.1 * self.speed / 5:  # Spawn rate based on speed
            self.meteors.append({
        'start_pos': random.randint(0, 13),  # Start from random column
        'start_time': current_time,
        'speed': self.speed * 20
            })

        # Remove expired meteors
        self.meteors = [m for m in self.meteors
        if current_time - m['start_time'] < 5.0]

        # Draw meteors
        for meteor in self.meteors:
            elapsed = current_time - meteor['start_time']
    pass
            current_row = int(elapsed * meteor['speed'] / 14)

            if current_row < 7:  # Still on keyboard
        for i in range(self.trail_length):
        trail_row = current_row - i
    pass
        if trail_row >= 0:
        key_id = trail_row * 14 + meteor['start_pos']
    pass
        if 0 <= key_id < OSIRIS_KEY_COUNT:
        intensity = (self.trail_length - i) / self.trail_length
    pass
        colors[key_id] = colors[key_id] + (self.color * intensity)

        return colors


class FireEffect(BaseEffect):
    """Flickering warm tones simulating fire"""

    def __init__(self, speed: int = 6, **params):
        super().__init__("Fire", speed=speed, **params)
        self.base_colors = [
            RGBColor(255, 0, 0),    # Red
            RGBColor(255, 69, 0),   # Orange Red
            RGBColor(255, 140, 0),  # Dark Orange
            RGBColor(255, 215, 0),  # Gold
        ]

    def get_colors(self) -> List[RGBColor]:
        if not self.is_running:
            return [Colors.BLACK] * OSIRIS_KEY_COUNT
    pass

        colors = []
        flicker_speed = self.speed * 2

        for key_id in range(OSIRIS_KEY_COUNT):
            # Create random flickering effect
    pass
            noise = random.random() * flicker_speed
            base_color = random.choice(self.base_colors)

            # Simulate fire intensity based on position (hotter at bottom)
            row = key_id // 14
            heat_intensity = max(0.3, 1 - (row / 7.0))

            # Add random flicker
            flicker_intensity = 0.7 + 0.3 * math.sin(time.time() * 10 + noise)
            total_intensity = heat_intensity * flicker_intensity

            colors.append(base_color * total_intensity)

        return colors


class OceanEffect(BaseEffect):
    """Flowing blue hues like water currents"""

    def __init__(self, speed: int = 4, **params):
        super().__init__("Ocean", speed=speed, **params)

    def get_colors(self) -> List[RGBColor]:
        if not self.is_running:
            return [Colors.BLACK] * OSIRIS_KEY_COUNT
    pass

        colors = []
        elapsed = time.time() - self.start_time
        wave_speed = self.speed

        for key_id in range(OSIRIS_KEY_COUNT):
            row = key_id // 14
    pass
            col = key_id % 14

            # Create flowing wave pattern
            wave1 = math.sin((col + elapsed * wave_speed) * 0.5) * 0.5 + 0.5
            wave2 = math.sin((row + elapsed * wave_speed * 0.7) * 0.8) * 0.5 + 0.5

            # Combine waves for complex pattern
            intensity = (wave1 + wave2) / 2

            # Ocean color gradient from deep blue to cyan
            hue = 180 + intensity * 60  # Blue to cyan range
            saturation = 0.8 + intensity * 0.2
            value = 0.5 + intensity * 0.5

            color = RGBColor.from_hsv(hue, saturation, value)
            colors.append(color)

        return colors


class StarlightEffect(BaseEffect):
    """Random twinkling of individual keys"""

    def __init__(self, color: RGBColor = Colors.WHITE, density: float = 0.1, **params):
        super().__init__("Starlight", color=color, **params)
        self.density = density  # Probability of star per frame
        self.stars: Dict[int, Dict[str, float]] = {}  # key_id: {start_time, duration}

    def get_colors(self) -> List[RGBColor]:
        colors = [Colors.BLACK] * OSIRIS_KEY_COUNT
        current_time = time.time()

        # Remove expired stars
        expired = [k for k, star in self.stars.items()
        if current_time - star['start_time'] > star['duration']]
        for k in expired:
            del self.stars[k]
    pass

        # Add new stars randomly
        for key_id in range(OSIRIS_KEY_COUNT):
            if key_id not in self.stars and random.random() < self.density / 100:
    pass
        self.stars[key_id] = {
        'start_time': current_time,
        'duration': random.uniform(0.5, 2.0)
        }

        # Draw twinkling stars
        for key_id, star in self.stars.items():
            elapsed = current_time - star['start_time']
    pass
            progress = elapsed / star['duration']

            # Twinkle with sine wave
            twinkle = math.sin(progress * math.pi * 4) * math.sin(progress * math.pi)
            intensity = max(0, twinkle)

            colors[key_id] = self.color * intensity

        return colors


class RainEffect(BaseEffect):
    """Random key lighting simulating rainfall"""

    def __init__(self, color: RGBColor = Colors.CYAN, intensity: float = 0.3, **params):
        super().__init__("Rain", color=color, **params)
        self.intensity = intensity
        self.raindrops: Dict[int, float] = {}  # key_id: start_time

    def get_colors(self) -> List[RGBColor]:
        colors = [Colors.BLACK] * OSIRIS_KEY_COUNT
        current_time = time.time()

        # Remove old raindrops
        self.raindrops = {k: t for k, t in self.raindrops.items()
        if current_time - t < 0.5}

        # Add new raindrops
        for key_id in range(OSIRIS_KEY_COUNT):
            if random.random() < self.intensity / 20:
    pass
        self.raindrops[key_id] = current_time

        # Draw raindrops with fade
        for key_id, start_time in self.raindrops.items():
            elapsed = current_time - start_time
    pass
            intensity = max(0, 1 - elapsed * 2)  # 0.5s fade
            colors[key_id] = self.color * intensity

        return colors


class MatrixCodeEffect(BaseEffect):
    """Vertical green cascades like falling code"""

    def __init__(self, color: RGBColor = Colors.GREEN, speed: int = 6, **params):
        super().__init__("Matrix Code", speed=speed, color=color, **params)
        self.streams: List[Dict[str, Any]] = []

    def get_colors(self) -> List[RGBColor]:
        colors = [Colors.BLACK] * OSIRIS_KEY_COUNT
        current_time = time.time()

        # Spawn new streams
        if random.random() < 0.3:
            col = random.randint(0, 13)
    pass
            self.streams.append({
        'col': col,
        'row': 0,
        'start_time': current_time,
        'length': random.randint(3, 8),
        'speed': self.speed + random.uniform(-1, 1)
            })

        # Update and draw streams
        for stream in self.streams[:]:  # Copy list for safe removal
            elapsed = current_time - stream['start_time']
            current_row = int(elapsed * stream['speed'])

            # Draw stream with fade
            for i in range(stream['length']):
        row = current_row - i
    pass
        if 0 <= row < 7:  # On keyboard
        key_id = row * 14 + stream['col']
        if 0 <= key_id < OSIRIS_KEY_COUNT:
        # Head is brightest, tail fades
    pass
        intensity = (stream['length'] - i) / stream['length']
        if i == 0:  # Head gets extra brightness
        intensity = 1.0
        colors[key_id] = self.color * intensity

            # Remove streams that have moved off screen
            if current_row - stream['length'] > 7:
        self.streams.remove(stream)
    pass

        return colors


class AudioVisualizerEffect(BaseEffect):
    """Keys pulse to music or sound input"""

    def __init__(self, color: RGBColor = Colors.PURPLE, sensitivity: float = 1.0, **params):
        super().__init__("Audio Visualizer", color=color, **params)
        self.sensitivity = sensitivity
        self.audio_level = 0.0  # Will be updated by audio input

    def update_audio_level(self, level: float):
        """Update current audio level (0.0 to 1.0)"""
        self.audio_level = max(0.0, min(1.0, level * self.sensitivity))

    def get_colors(self) -> List[RGBColor]:
        if not self.is_running:
            return [Colors.BLACK] * OSIRIS_KEY_COUNT
    pass

        # Create visualizer bars based on audio level
        colors = []
        bars = 14  # Number of visualizer bars (columns)

        for key_id in range(OSIRIS_KEY_COUNT):
            col = key_id % 14
    pass
            row = key_id // 14

            # Each column represents a frequency band
            band_intensity = self.audio_level * (1 + random.uniform(-0.2, 0.2))  # Add variation
            bar_height = int(band_intensity * 7)  # Scale to keyboard rows

            # Light up keys from bottom to current audio level
            if row >= (7 - bar_height):
        intensity = 1.0 - (row - (7 - bar_height)) / max(1, bar_height)
    pass
        colors.append(self.color * intensity)
            else:
    pass
    pass
    pass
        colors.append(Colors.BLACK)

        return colors


class SystemLoadEffect(BaseEffect):
    """Color changes based on CPU/GPU usage"""

    def __init__(self, **params):
        super().__init__("System Load Monitor", **params)
        self.cpu_usage = 0.0
        self.gpu_usage = 0.0

    def update_system_load(self, cpu: float, gpu: float = 0.0):
        """Update system load values (0.0 to 1.0)"""
        self.cpu_usage = max(0.0, min(1.0, cpu))
        self.gpu_usage = max(0.0, min(1.0, gpu))

    def get_colors(self) -> List[RGBColor]:
        if not self.is_running:
            return [Colors.BLACK] * OSIRIS_KEY_COUNT
    pass

        colors = []

        # Color coding: Green = low load, Yellow = medium, Red = high
        for key_id in range(OSIRIS_KEY_COUNT):
            # Left half shows CPU, right half shows GPU (or CPU if no GPU data)
    pass
            col = key_id % 14

            if col < 7:  # CPU side
        load = self.cpu_usage
            else:  # GPU side
        load = self.gpu_usage if self.gpu_usage > 0 else self.cpu_usage

            # Color based on load level
            if load < 0.3:  # Low load - green
        hue = 120
            elif load < 0.7:  # Medium load - yellow
        hue = 60
            else:  # High load - red
        hue = 0

            color = RGBColor.from_hsv(hue, 1.0, load)
            colors.append(color)

        return colors


class PerKeyCustomEffect(BaseEffect):
    """Assign unique colors/effects to each key"""

    def __init__(self, key_colors: Optional[Dict[int, RGBColor]] = None, **params):
        super().__init__("Per-Key Custom", **params)
        self.key_colors = key_colors or {}

    def set_key_color(self, key_id: int, color: RGBColor):
        """Set color for specific key"""
        if 0 <= key_id < OSIRIS_KEY_COUNT:
            self.key_colors[key_id] = color
    pass

    def get_colors(self) -> List[RGBColor]:
        colors = []

        for key_id in range(OSIRIS_KEY_COUNT):
            if key_id in self.key_colors:
    pass
        colors.append(self.key_colors[key_id])
            else:
    pass
    pass
    pass
        colors.append(Colors.BLACK)

        return colors


class CountdownEffect(BaseEffect):
    """Visual countdown using lighting"""

    def __init__(self, duration: int = 60, color: RGBColor = Colors.ORANGE, **params):
        super().__init__("Countdown", color=color, **params)
        self.duration = duration  # seconds
        self.countdown_start = None

    def start_countdown(self, duration: int = None):
        """Start countdown timer"""
        if duration:
            self.duration = duration
    pass
        self.countdown_start = time.time()
        self.start()

    def get_colors(self) -> List[RGBColor]:
        if not self.is_running or not self.countdown_start:
            return [Colors.BLACK] * OSIRIS_KEY_COUNT
    pass

        elapsed = time.time() - self.countdown_start
        remaining = max(0, self.duration - elapsed)
        progress = remaining / self.duration

        # Stop when countdown reaches zero
        if remaining <= 0:
            self.stop()
    pass
            return [Colors.RED] * OSIRIS_KEY_COUNT  # Flash red when done

        # Light up keys based on remaining time
        keys_to_light = int(progress * OSIRIS_KEY_COUNT)

        colors = []
        for i in range(OSIRIS_KEY_COUNT):
            if i < keys_to_light:
    pass
        # Color shifts from green to red as time runs out
        hue = 120 * progress  # Green (120) to red (0)
        color = RGBColor.from_hsv(hue, 1.0, 1.0)
        colors.append(color)
            else:
    pass
    pass
    pass
        colors.append(Colors.BLACK)

        return colors


class TypeLightingEffect(BaseEffect):
    """Light spreads from keypress horizontally or vertically"""

    def __init__(self, color: RGBColor = Colors.WHITE, direction: str = "horizontal",
        spread_speed: float = 5.0, **params):
        super().__init__("Type Lighting", color=color, **params)
        self.direction = direction  # "horizontal" or "vertical"
        self.spread_speed = spread_speed
        self.active_spreads: List[Dict[str, Any]] = []

    def trigger_spread(self, key_id: int):
        """Trigger spreading effect from key"""
        if 0 <= key_id < OSIRIS_KEY_COUNT:
            self.active_spreads.append({
    pass
        'center_key': key_id,
        'start_time': time.time(),
        'max_distance': 10.0
            })

    def get_colors(self) -> List[RGBColor]:
        colors = [Colors.BLACK] * OSIRIS_KEY_COUNT
        current_time = time.time()

        # Remove expired spreads
        self.active_spreads = [s for s in self.active_spreads
        if current_time - s['start_time'] < s['max_distance'] / self.spread_speed]

        # Apply spreading effects
        for spread in self.active_spreads:
            elapsed = current_time - spread['start_time']
    pass
            current_distance = elapsed * self.spread_speed

            center_key = spread['center_key']
            center_row = center_key // 14
            center_col = center_key % 14

            for key_id in range(OSIRIS_KEY_COUNT):
        key_row = key_id // 14
    pass
        key_col = key_id % 14

        if self.direction == "horizontal":
        distance = abs(key_col - center_col) if key_row == center_row else float('inf')
    pass
        else:  # vertical
        distance = abs(key_row - center_row) if key_col == center_col else float('inf')

        if distance <= current_distance and distance < spread['max_distance']:
        intensity = max(0, 1 - distance / current_distance) if current_distance > 0 else 1
    pass
        colors[key_id] = colors[key_id] + (self.color * intensity)

        return colors


class TornadoEffect(BaseEffect):
    """Spiral-like motion across keyboard"""

    def __init__(self, color: RGBColor = Colors.PURPLE, speed: int = 5, **params):
        super().__init__("Tornado", speed=speed, color=color, **params)
        self.center_x = 7  # Center column
        self.center_y = 3  # Center row

    def get_colors(self) -> List[RGBColor]:
        if not self.is_running:
            return [Colors.BLACK] * OSIRIS_KEY_COUNT
    pass

        colors = [Colors.BLACK] * OSIRIS_KEY_COUNT
        elapsed = time.time() - self.start_time
        rotation_speed = self.speed * 2

        for key_id in range(OSIRIS_KEY_COUNT):
            col = key_id % 14
    pass
            row = key_id // 14

            # Calculate distance from center
            dx = col - self.center_x
            dy = row - self.center_y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance > 0:
        # Calculate angle
    pass
        angle = math.atan2(dy, dx)

        # Create spiral pattern
        spiral_angle = angle + (distance * 0.5) - (elapsed * rotation_speed)
        spiral_intensity = (math.sin(spiral_angle) + 1) / 2

        # Fade with distance
        distance_fade = max(0, 1 - distance / 8)

        total_intensity = spiral_intensity * distance_fade
        colors[key_id] = self.color * total_intensity

        return colors


class LightningEffect(BaseEffect):
    """Sudden flashes across zones or keys"""

    def __init__(self, color: RGBColor = Colors.WHITE, flash_duration: float = 0.1, **params):
        super().__init__("Lightning", color=color, **params)
        self.flash_duration = flash_duration
        self.lightning_strikes: List[Dict[str, Any]] = []

    def trigger_lightning(self):
        """Trigger a lightning strike"""
        # Create random lightning pattern
        strike_keys = random.sample(range(OSIRIS_KEY_COUNT), random.randint(5, 15))
        self.lightning_strikes.append({
            'keys': strike_keys,
            'start_time': time.time(),
            'duration': self.flash_duration + random.uniform(0, 0.05)
        })

    def get_colors(self) -> List[RGBColor]:
        colors = [Colors.BLACK] * OSIRIS_KEY_COUNT
        current_time = time.time()

        # Randomly trigger lightning
        if random.random() < 0.02:  # 2% chance per frame
            self.trigger_lightning()

        # Remove expired strikes
        self.lightning_strikes = [s for s in self.lightning_strikes
        if current_time - s['start_time'] < s['duration']]

        # Draw lightning strikes
        for strike in self.lightning_strikes:
            elapsed = current_time - strike['start_time']
    pass
            progress = elapsed / strike['duration']

            # Flash intensity with quick fade
            intensity = max(0, 1 - progress * 3)  # Quick fade

            for key_id in strike['keys']:
        if 0 <= key_id < OSIRIS_KEY_COUNT:
    pass
        colors[key_id] = self.color * intensity

        return colors


# Effect registry for easy access
EFFECT_REGISTRY = {
    'static_color': StaticColorEffect,
    'color_shift': ColorShiftEffect,
    'rainbow_wave': RainbowWaveEffect,
    'breathing': BreathingEffect,
    'reactive_keypress': ReactiveKeypressEffect,
    'ripple': RippleEffect,
    'pulse_wave': PulseWaveEffect,
    'scanning_beam': ScanningBeamEffect,
    'snake': SnakeEffect,
    'meteor': MeteorEffect,
    'fire': FireEffect,
    'ocean': OceanEffect,
    'starlight': StarlightEffect,
    'rain': RainEffect,
    'matrix_code': MatrixCodeEffect,
    'audio_visualizer': AudioVisualizerEffect,
    'system_load': SystemLoadEffect,
    'per_key_custom': PerKeyCustomEffect,
    'countdown': CountdownEffect,
    'type_lighting': TypeLightingEffect,
    'tornado': TornadoEffect,
    'lightning': LightningEffect,
}

# Categories for UI organization
EFFECT_CATEGORIES = {
    'Static Effects': ['static_color', 'per_key_custom'],
    'Color Transitions': ['color_shift', 'breathing', 'rainbow_wave'],
    'Interactive Effects': ['reactive_keypress', 'ripple', 'type_lighting'],
    'Wave Effects': ['pulse_wave', 'scanning_beam', 'ocean'],
    'Particle Effects': ['snake', 'meteor', 'starlight', 'rain', 'lightning'],
    'Ambient Effects': ['fire', 'matrix_code', 'tornado'],
    'System Effects': ['audio_visualizer', 'system_load', 'countdown'],
}

# Effect compatibility with OSIRIS hardware
OSIRIS_COMPATIBLE_EFFECTS = list(EFFECT_REGISTRY.keys())  # All effects compatible!

# Performance ratings (1=light, 5=heavy)
EFFECT_PERFORMANCE_RATINGS = {
    'static_color': 1,
    'color_shift': 1,
    'breathing': 1,
    'rainbow_wave': 2,
    'reactive_keypress': 2,
    'per_key_custom': 1,
    'pulse_wave': 3,
    'scanning_beam': 2,
    'ripple': 3,
    'snake': 2,
    'meteor': 3,
    'fire': 4,
    'ocean': 3,
    'starlight': 2,
    'rain': 3,
    'matrix_code': 4,
    'audio_visualizer': 4,
    'system_load': 2,
    'countdown': 1,
    'type_lighting': 3,
    'tornado': 4,
    'lightning': 3,
}


def get_effect_by_name(name: str, **params) -> Optional[BaseEffect]:
    """
    Create effect instance by name

    Args:
        name: Effect name from registry
        **params: Effect parameters

    Returns:
        Optional[BaseEffect]: Effect instance or None if not found
    """
    effect_class = EFFECT_REGISTRY.get(name.lower())
    if effect_class:
        return effect_class(**params)
    pass
    return None


def get_available_effects() -> List[str]:
    """Get list of all available effect names"""
    return list(EFFECT_REGISTRY.keys())


def get_effects_by_category(category: str) -> List[str]:
    """Get effects in specific category"""
    return EFFECT_CATEGORIES.get(category, [])


def is_effect_osiris_compatible(effect_name: str) -> bool:
    """Check if effect is compatible with OSIRIS hardware"""
    return effect_name.lower() in OSIRIS_COMPATIBLE_EFFECTS


def get_effect_performance_rating(effect_name: str) -> int:
    """Get performance rating for effect (1=light, 5=heavy)"""
    return EFFECT_PERFORMANCE_RATINGS.get(effect_name.lower(), 3)


def create_default_effect_set() -> Dict[str, BaseEffect]:
    """Create set of commonly used effects with default settings"""
    return {
        'static_white': StaticColorEffect(Colors.WHITE),
        'breathing_blue': BreathingEffect(Colors.BLUE, speed=3),
        'rainbow_wave': RainbowWaveEffect(speed=5),
        'reactive_cyan': ReactiveKeypressEffect(Colors.CYAN),
        'fire_effect': FireEffect(speed=6),
        'matrix_green': MatrixCodeEffect(Colors.GREEN, speed=4),
    }
