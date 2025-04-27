# src/components/dashboard.py

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class Dashboard:
    def __init__(self, parent):
        self.parent = parent
        
        # Create layout
        self.setup_layout()
        
        # Initialize data
        self.depth_history = []
        self.temp_history = []
        self.time_points = []
        
    def setup_layout(self):
        # Create main layout frames
        self.video_frame = ctk.CTkFrame(self.parent)
        self.video_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.metrics_frame = ctk.CTkFrame(self.parent)
        self.metrics_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.graphs_frame = ctk.CTkFrame(self.parent)
        self.graphs_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Configure grid weights
        self.parent.grid_columnconfigure(0, weight=3)
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.grid_rowconfigure(0, weight=2)
        self.parent.grid_rowconfigure(1, weight=1)
        
        # Setup metric displays
        self.setup_metrics()
        self.setup_graphs()
        
    def setup_metrics(self):
        # Depth display
        self.depth_label = ctk.CTkLabel(self.metrics_frame, text="Depth (m)")
        self.depth_label.pack(pady=5)
        self.depth_value = ctk.CTkLabel(self.metrics_frame, text="0.0", font=("Arial", 24))
        self.depth_value.pack(pady=5)
        
        # Temperature display
        self.temp_label = ctk.CTkLabel(self.metrics_frame, text="Temperature (°C)")
        self.temp_label.pack(pady=5)
        self.temp_value = ctk.CTkLabel(self.metrics_frame, text="0.0", font=("Arial", 24))
        self.temp_value.pack(pady=5)
        
        # Battery display
        self.battery_label = ctk.CTkLabel(self.metrics_frame, text="Battery (%)")
        self.battery_label.pack(pady=5)
        self.battery_progress = ctk.CTkProgressBar(self.metrics_frame)
        self.battery_progress.pack(pady=5)
        self.battery_progress.set(1.0)
        
    def setup_graphs(self):
        # Create matplotlib figure for depth and temperature history
        self.fig = Figure(figsize=(6, 2), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graphs_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def update_display(self, telemetry_data):
        # Update metric displays
        self.depth_value.configure(text=f"{telemetry_data.get('depth', 0):.1f}")
        self.temp_value.configure(text=f"{telemetry_data.get('temperature', 0):.1f}")
        self.battery_progress.set(telemetry_data.get('battery', 100) / 100)
        
        # Update history data
        self.depth_history.append(telemetry_data.get('depth', 0))
        self.temp_history.append(telemetry_data.get('temperature', 0))
        
        # Keep last 100 points
        if len(self.depth_history) > 100:
            self.depth_history.pop(0)
            self.temp_history.pop(0)
        
        # Update graph
        self.update_graph()
        
    def update_graph(self):
        self.ax.clear()
        x = range(len(self.depth_history))
        self.ax.plot(x, self.depth_history, label='Depth')
        self.ax.plot(x, self.temp_history, label='Temperature')
        self.ax.legend()
        self.ax.set_title('Telemetry History')
        self.canvas.draw()