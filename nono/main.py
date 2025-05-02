from PyQt6 import QtWidgets, QtCore, QtGui
from gui import Ui_Form
from serialcont import SerialController
import sys
import pygame
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class UpdateSignals(QtCore.QObject):
    update_values = QtCore.pyqtSignal(list)

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Robot Controller")
        self.apply_stylesheet()
        self.controller = None
        self.signals = UpdateSignals()
        self.signals.update_values.connect(self.update_labels)
        
        # Load both controller and pico status icons
        self.icon_on = QtGui.QPixmap(resource_path("on2.png"))
        self.icon_off = QtGui.QPixmap(resource_path("off2.png"))
        self.pico_on = QtGui.QPixmap(resource_path("on.png"))
        self.pico_off = QtGui.QPixmap(resource_path("off.png"))
        
        # Scale all icons
        self.icon_on = self.icon_on.scaled(70, 70, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.icon_off = self.icon_off.scaled(70, 70, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        # Scale Pico icons maintaining aspect ratio
        self.pico_on = self.pico_on.scaled(40, 70, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.pico_off = self.pico_off.scaled(40, 70, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        
        # Setup status check timer
        self.status_timer = QtCore.QTimer()
        self.status_timer.timeout.connect(self.check_controller_status)
        self.status_timer.start(1000)  # Changed from 3000 to 1000 for 1 second interval
        
        # Initial icons
        self.update_status_icon(False)
        self.update_pico_icon(False)
        
        # Connect buttons
        self.ui.pushButton.clicked.connect(self.start_controller)
        self.ui.pushButton_2.clicked.connect(self.stop_controller)

    def apply_stylesheet(self):
        style = """
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QPushButton {
                background-color: #0d47a1;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                min-width: 100px;
                color: white;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0a3d91;
            }
            QLabel {
                padding: 5px;
                border-radius: 5px;
            }
            QLabel[objectName^="label_"][objectName!="label_6"] {
                background-color: #424242;
                padding: 8px;
                margin: 2px;
            }
            QLabel[objectName^="label_7"], 
            QLabel[objectName^="label_8"],
            QLabel[objectName^="label_9"],
            QLabel[objectName^="label_10"],
            QLabel[objectName^="label_11"],
            QLabel[objectName^="label_12"] {
                background-color: #1e88e5;
                min-width: 80px;
                text-align: center;
            }
            QLabel#title_label {
                color: #ffffff;
                padding: 15px;
                margin: 15px;
            }
        """
        self.setStyleSheet(style)

    def update_status_icon(self, is_connected):
        icon = self.icon_on if is_connected else self.icon_off
        self.ui.controller_status.setPixmap(icon)
        
    def update_pico_icon(self, is_connected):
        icon = self.pico_on if is_connected else self.pico_off
        self.ui.pico_status.setPixmap(icon)
        
    def check_controller_status(self):
        try:
            # Check controller - only reinitialize if not already running
            is_controller_connected = False
            if not self.controller:
                pygame.joystick.quit()
                pygame.joystick.init()
                if pygame.joystick.get_count() > 0:
                    joystick = pygame.joystick.Joystick(0)
                    joystick.init()
                    is_controller_connected = True
            else:
                is_controller_connected = True
            
            # Check Pico
            is_pico_connected = False
            if self.controller and self.controller.ser and self.controller.ser.is_open:
                is_pico_connected = True
            
            self.update_status_icon(is_controller_connected)
            self.update_pico_icon(is_pico_connected)
            
        except:
            self.update_status_icon(False)
            self.update_pico_icon(False)
        
    def start_controller(self):
        if not self.controller:
            try:
                self.controller = SerialController(self.signals)
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", str(e))
                self.clear_labels()
    
    def stop_controller(self):
        if self.controller:
            self.controller.stop()
            self.controller = None
            self.clear_labels()
            
    def clear_labels(self):
        for label in [self.ui.label_7, self.ui.label_8, self.ui.label_9, 
                     self.ui.label_10, self.ui.label_11, self.ui.label_12]:
            label.setText("None")
            
    @QtCore.pyqtSlot(list)
    def update_labels(self, results):
        self.ui.label_7.setText(str(results[0]))
        self.ui.label_8.setText(str(results[1]))
        self.ui.label_9.setText(str(results[2]))
        self.ui.label_10.setText(str(results[3]))
        self.ui.label_11.setText(str(results[4]))
        self.ui.label_12.setText(str(results[5]))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
