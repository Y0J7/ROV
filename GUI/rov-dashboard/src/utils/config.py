# Configuration settings for the ROV dashboard application

# Window settings
WINDOW_TITLE = "ROV Dashboard"
WINDOW_SIZE = (1280, 800)
WINDOW_MIN_SIZE = (800, 600)

# Theme settings
THEME = {
    "dark_mode": True,
    "accent_color": "blue",
    "font_family": "Roboto",
    "font_size": 12
}

# Video settings
VIDEO = {
    "main_camera_url": 0,  # Use 0 for default webcam or URL for IP camera
    "secondary_camera_url": 1,
    "frame_rate": 30,
    "resolution": (640, 480),
    "screenshot_path": "./screenshots/"
}

# Telemetry settings
TELEMETRY = {
    "update_interval": 0.1,  # seconds
    "max_history_points": 100,
    "sensors": {
        "depth": {"min": 0, "max": 100, "unit": "m"},
        "temperature": {"min": -10, "max": 40, "unit": "°C"},
        "pressure": {"min": 0, "max": 1000, "unit": "kPa"},
        "humidity": {"min": 0, "max": 100, "unit": "%"},
        "heading": {"min": 0, "max": 360, "unit": "°"},
        "battery": {"min": 0, "max": 100, "unit": "%"}
    }
}

# Control settings
CONTROLS = {
    "joystick": {
        "deadzone": 0.05,
        "sensitivity": 1.0
    },
    "depth_control": {
        "step": 0.1,
        "max_rate": 1.0
    },
    "motor_limits": {
        "max_thrust": 1.0,
        "max_turn_rate": 0.8
    }
}

# Data logging
LOGGING = {
    "enabled": True,
    "log_path": "./logs/",
    "log_interval": 1.0,  # seconds
    "max_log_size": 1024 * 1024 * 10  # 10 MB
}