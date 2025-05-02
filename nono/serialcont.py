import pygame
import time
import serial
import threading

class SerialController:
    def __init__(self, signals):
        pygame.init()
        pygame.joystick.init()
        
        self.arry = [0, 0, 0, 0, 0, 0]
        self.x = []
        self.buttons = [0] * 16
        self.prev_buttons = [0] * 16
        self.states = [0] * 4
        self.speed = 0
        self.prev_states = [0, 0, 0, 0]
        self.running = True
        self.results = ["N", 0, 0, 0, 0, 0]
        self.prev_results = ["N", 0, 0, 0, 0, 0]  # Add this line
        self.signals = signals
        
        # Initialize serial with retry
        self.ser = self.initialize_serial()
        
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            try:
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
                self.thread = threading.Thread(target=self.run)
                self.thread.daemon = True
                self.thread.start()
            except pygame.error:
                print("Failed to initialize joystick")

    def initialize_serial(self, max_attempts=5):
        for attempt in range(max_attempts):
            try:
                if hasattr(self, 'ser') and self.ser and self.ser.is_open:
                    self.ser.close()
                    time.sleep(1)
                ser = serial.Serial("COM3", 115200)
                return ser
            except (serial.SerialException, OSError):
                time.sleep(2)  # Longer delay between attempts
                if attempt == max_attempts - 1:
                    raise Exception("Failed to open serial port after multiple attempts")
        return None

    def run(self):
        while self.running:
            self.update()
            time.sleep(0.05)  # Reduced from 0.1 to 0.05
    
    def update(self):
        try:
            if not self.joystick:
                return
                
            pygame.event.pump()
            
            # Check if joystick is still connected
            if not self.joystick.get_init():
                self.joystick.init()
                
            for i in range(self.joystick.get_numaxes()):
                axis = self.joystick.get_axis(i)
                self.buttons[i] = self.joystick.get_button(i)
                self.arry[i] = axis
            
            # Check stop button first
            if self.joystick.get_button(4) == 1:
                self.stop()
                return
            
            motion = "N"
            x = self.arry[:4]
            
            # Motion detection logic
            if x[1] < -0.4: motion = "F"
            elif x[1] > 0.4: motion = "B"
            elif x[0] < -0.4: motion = "L"
            elif x[0] > 0.4: motion = "R"
            elif x[2] < -0.4: motion = "l"
            elif x[2] > 0.4: motion = "r"
            elif x[3] < -0.4: motion = "u"
            elif x[3] > 0.4: motion = "d"
            
            # Button state updates
            if self.buttons != self.prev_buttons:
                for i in range(4):
                    if self.buttons[i] == 1:
                        self.states[i] = int(not self.states[i])
                self.prev_buttons = self.buttons.copy()
            
            # Speed control
            if self.joystick.get_button(11) == 1 and self.speed < 100:
                self.speed += 10
            elif self.joystick.get_button(12) == 1 and self.speed > 0:
                self.speed -= 10
            
            # Update results and emit signal
            self.results = [motion, self.states[0], self.states[1], self.states[2], self.states[3], self.speed]
            self.signals.update_values.emit(self.results)
            
            # Only send if data changed
            if self.results != self.prev_results:
                data = f"{self.results[0]},{self.results[1]},{self.results[2]},{self.results[3]},{self.results[4]},{self.results[5]}%\r\n"
                self.ser.write(data.encode())
                # Only flush when necessary
                if self.results[0] != self.prev_results[0] or self.speed != self.prev_results[5]:
                    self.ser.flush()
                self.prev_results = self.results.copy()
        
        except pygame.error:
            self.stop()
            return
            
    def stop(self):
        if self.running:
            self.running = False
            results = ["w", 0, 0, 0, 0, 0]
            try:
                if hasattr(self, 'ser') and self.ser and self.ser.is_open:
                    self.ser.write(f"{results[0]},{results[1]},{results[2]},{results[3]},{results[4]},{results[5]}%\r\n".encode())
                    self.ser.flush()
                    self.ser.close()
                    time.sleep(1)  # Wait for port to fully close
            except:
                pass
                
            if self.joystick and self.joystick.get_init():
                self.joystick.quit()
            pygame.quit()

if __name__ == "__main__":
    SerialController()

