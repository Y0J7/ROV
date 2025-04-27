def format_telemetry_data(data):
    """Format telemetry data for display."""
    formatted_data = {key: f"{value:.2f}" for key, value in data.items()}
    return formatted_data

def validate_input(value, min_value, max_value):
    """Validate user input within a specified range."""
    if min_value <= value <= max_value:
        return True
    return False

def update_display(element, value):
    """Update the display element with a new value."""
    element.set_text(value)