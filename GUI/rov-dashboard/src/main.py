# filepath: rov-dashboard/src/main.py

import customtkinter as ctk
import utils.config as config
from components.dashboard import Dashboard
from components.controls import Controls
from components.telemetry import Telemetry
from components.video_feed import VideoFeed

class ROVApplication:
    def __init__(self):
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Create main window
        self.window = ctk.CTk()
        self.window.title(config.WINDOW_TITLE)
        self.window.geometry(f"{config.WINDOW_SIZE[0]}x{config.WINDOW_SIZE[1]}")

        # Create main container
        self.container = ctk.CTkTabview(self.window)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        # Add tabs
        self.container.add("Dashboard")
        self.container.add("Controls")
        self.container.add("Settings")

        # Initialize components
        self.dashboard = Dashboard(self.container.tab("Dashboard"))
        self.controls = Controls(self.container.tab("Controls"))
        self.telemetry = Telemetry(self.dashboard)
        self.video_feed = VideoFeed(self.dashboard)

    def run(self):
        self.window.mainloop()

def main():
    app = ROVApplication()
    app.run()

if __name__ == "__main__":
    main()