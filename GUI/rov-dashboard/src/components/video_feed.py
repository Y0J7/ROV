# filepath: rov-dashboard/src/components/video_feed.py

import cv2
import customtkinter as ctk
from PIL import Image, ImageTk
import threading
import time

class VideoFeed:
    def __init__(self, parent):
        self.parent = parent
        self.is_streaming = False
        self.frame_label = ctk.CTkLabel(self.parent.video_frame, text="")
        self.frame_label.pack(expand=True, fill="both")
        
        # Camera selection
        self.camera_frame = ctk.CTkFrame(self.parent.video_frame)
        self.camera_frame.pack(fill="x", padx=5, pady=5)
        
        self.camera_label = ctk.CTkLabel(self.camera_frame, text="Camera:")
        self.camera_label.pack(side="left", padx=5)
        
        self.camera_select = ctk.CTkOptionMenu(
            self.camera_frame,
            values=["Main Camera", "Secondary Camera"],
            command=self.switch_camera
        )
        self.camera_select.pack(side="left", padx=5)
        
        # Screenshot button
        self.screenshot_btn = ctk.CTkButton(
            self.camera_frame,
            text="Screenshot",
            command=self.take_screenshot
        )
        self.screenshot_btn.pack(side="right", padx=5)
        
        self.video_source = 0  # Default camera
        self.cap = None
        
    def start_stream(self):
        if not self.is_streaming:
            self.cap = cv2.VideoCapture(self.video_source)
            self.is_streaming = True
            self.thread = threading.Thread(target=self._stream_loop)
            self.thread.daemon = True
            self.thread.start()
            
    def stop_stream(self):
        self.is_streaming = False
        if self.cap:
            self.cap.release()
            
    def _stream_loop(self):
        while self.is_streaming:
            ret, frame = self.cap.read()
            if ret:
                # Convert frame to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert to PhotoImage
                image = Image.fromarray(frame_rgb)
                # Resize to fit the window while maintaining aspect ratio
                display_size = (640, 480)
                image.thumbnail(display_size, Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image=image)
                
                # Update label
                self.frame_label.configure(image=photo)
                self.frame_label.image = photo
            
            time.sleep(0.03)  # Limit to ~30 FPS
            
    def switch_camera(self, selection):
        was_streaming = self.is_streaming
        if was_streaming:
            self.stop_stream()
        
        if selection == "Main Camera":
            self.video_source = 0
        else:
            self.video_source = 1
            
        if was_streaming:
            self.start_stream()
            
    def take_screenshot(self):
        if self.cap and self.is_streaming:
            ret, frame = self.cap.read()
            if ret:
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = f"screenshot_{timestamp}.jpg"
                cv2.imwrite(filename, frame)
                print(f"Screenshot saved as {filename}")