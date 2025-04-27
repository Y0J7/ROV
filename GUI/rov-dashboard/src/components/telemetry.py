import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time

class Telemetry:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.data = {
            'depth': [],
            'temperature': [],
            'heading': 0,
            'battery': 100,
            'pressure': 0,
            'humidity': 0
        }
        self.timestamps = []
        self.max_history = 100
        
    def update_data(self, new_data):
        """Update telemetry data with new sensor readings"""
        timestamp = time.time()
        self.timestamps.append(timestamp)
        
        for key, value in new_data.items():
            if key in ['depth', 'temperature']:
                self.data[key].append(value)
                if len(self.data[key]) > self.max_history:
                    self.data[key].pop(0)
                    self.timestamps.pop(0)
            else:
                self.data[key] = value
        
        # Update dashboard display
        self.dashboard.update_display(self.data)
        
    def get_latest_values(self):
        """Get the most recent sensor readings"""
        latest = {}
        for key, value in self.data.items():
            if isinstance(value, list):
                latest[key] = value[-1] if value else 0
            else:
                latest[key] = value
        return latest
        
    def get_history(self, sensor_type):
        """Get historical data for a specific sensor"""
        if sensor_type in self.data and isinstance(self.data[sensor_type], list):
            return {
                'timestamps': self.timestamps,
                'values': self.data[sensor_type]
            }
        return None
        
    def clear_history(self):
        """Clear historical data"""
        for key in self.data:
            if isinstance(self.data[key], list):
                self.data[key] = []
        self.timestamps = []