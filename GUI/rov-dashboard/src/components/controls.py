# controls.py

import customtkinter as ctk
import math

class JoystickCanvas(ctk.CTkCanvas):
    def __init__(self, parent, size=100, **kwargs):
        super().__init__(parent, width=size, height=size, **kwargs)
        self.size = size
        self.center = size // 2
        self.radius = (size - 20) // 2
        self.stick_pos = (self.center, self.center)
        self.callback = None
        
        self.create_oval(10, 10, size-10, size-10, outline='gray')
        self.stick = self.create_oval(
            self.center-5, self.center-5,
            self.center+5, self.center+5,
            fill='blue'
        )
        
        self.bind('<B1-Motion>', self.on_drag)
        self.bind('<ButtonRelease-1>', self.on_release)
        
    def on_drag(self, event):
        x = event.x - self.center
        y = event.y - self.center
        distance = math.sqrt(x*x + y*y)
        
        if distance > self.radius:
            x = x * self.radius / distance
            y = y * self.radius / distance
            
        self.stick_pos = (x + self.center, y + self.center)
        self.coords(
            self.stick,
            self.stick_pos[0]-5, self.stick_pos[1]-5,
            self.stick_pos[0]+5, self.stick_pos[1]+5
        )
        
        # Calculate normalized values (-1 to 1)
        nx = x / self.radius
        ny = -y / self.radius  # Invert Y for intuitive control
        
        if self.callback:
            self.callback(nx, ny)
            
    def on_release(self, event):
        self.stick_pos = (self.center, self.center)
        self.coords(
            self.stick,
            self.center-5, self.center-5,
            self.center+5, self.center+5
        )
        if self.callback:
            self.callback(0, 0)

class Controls:
    def __init__(self, parent):
        self.parent = parent
        self.control_state = {
            'thrust': 0,
            'steering': 0,
            'depth': 0,
            'lights': False,
            'manipulator': False
        }
        
        self.setup_layout()
        
    def setup_layout(self):
        # Movement controls frame
        self.movement_frame = ctk.CTkFrame(self.parent)
        self.movement_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Movement joystick
        self.movement_label = ctk.CTkLabel(self.movement_frame, text="Movement Control")
        self.movement_label.pack(pady=5)
        self.movement_stick = JoystickCanvas(self.movement_frame, size=200)
        self.movement_stick.pack(pady=10)
        self.movement_stick.callback = self.on_movement
        
        # Vertical controls frame
        self.vertical_frame = ctk.CTkFrame(self.parent)
        self.vertical_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Depth control slider
        self.depth_label = ctk.CTkLabel(self.vertical_frame, text="Depth Control")
        self.depth_label.pack(pady=5)
        self.depth_slider = ctk.CTkSlider(
            self.vertical_frame,
            orientation="vertical",
            height=200,
            from_=1.0,
            to=-1.0
        )
        self.depth_slider.pack(pady=10)
        self.depth_slider.set(0)
        self.depth_slider.configure(command=self.on_depth)
        
        # Auxiliary controls frame
        self.aux_frame = ctk.CTkFrame(self.parent)
        self.aux_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Lights toggle
        self.lights_switch = ctk.CTkSwitch(
            self.aux_frame,
            text="Lights",
            command=self.on_lights
        )
        self.lights_switch.pack(side="left", padx=20)
        
        # Manipulator toggle
        self.manipulator_switch = ctk.CTkSwitch(
            self.aux_frame,
            text="Manipulator",
            command=self.on_manipulator
        )
        self.manipulator_switch.pack(side="left", padx=20)
        
        # Configure grid weights
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.grid_rowconfigure(0, weight=3)
        self.parent.grid_rowconfigure(1, weight=1)
        
    def on_movement(self, x, y):
        self.control_state['thrust'] = y
        self.control_state['steering'] = x
        self.update_control_state()
        
    def on_depth(self, value):
        self.control_state['depth'] = float(value)
        self.update_control_state()
        
    def on_lights(self):
        self.control_state['lights'] = self.lights_switch.get()
        self.update_control_state()
        
    def on_manipulator(self):
        self.control_state['manipulator'] = self.manipulator_switch.get()
        self.update_control_state()
        
    def update_control_state(self):
        # This method would typically send the control state to the ROV
        print("Control state updated:", self.control_state)