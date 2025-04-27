import serial
import time
import keyboard

states = [0, 0, 0, 0]
prev_states = [0, 0, 0, 0]
speed = 0
ser = serial.Serial("COM3",112500)


while True:
    keys = 0
    motion = "N"
    prev_keys = [0, 0, 0, 0]
    
    if keys != prev_keys:
        if keyboard.get_hotkey_name() == "w":
            motion = "F"
        if keyboard.get_hotkey_name() == "s":
            motion = "B"
        if keyboard.get_hotkey_name() == "a":
            motion = "L"
        if keyboard.get_hotkey_name() == "d":
            motion = "R"
#------------------------------------------------------
        if keyboard.get_hotkey_name() == "1":
            states[0] = 1
        if keyboard.get_hotkey_name() == "2":
            states[1] = 1 
        if keyboard.get_hotkey_name() == "3":
            states[2] = 1 
        if keyboard.get_hotkey_name() == "4":
            states[3] = 1 
        if keyboard.get_hotkey_name() == "5":
            states[0] = 0
        if keyboard.get_hotkey_name() == "6":
            states[1] = 0
        if keyboard.get_hotkey_name() == "7":
            states[2] = 0
        if keyboard.get_hotkey_name() == "8":
            states[3] = 0
#------------------------------------------------------
        if keyboard.get_hotkey_name() == "up":
            if speed < 100:
                speed += 10
        if keyboard.get_hotkey_name() == "down":
            if speed > 0:
                speed -= 10
    
    results = [motion, states[0], states[1], states[2], states[3], speed]
    if results != prev_states:
        prev_states = results.copy()
        ser.write(f"{results[0]},{results[1]},{results[2]},{results[3]},{results[4]},{results[5]}%\r\n".encode())
        ser.flush()
        print(f"{results[0]},{results[1]},{results[2]},{results[3]},{results[4]},{results[5]}%")
        time.sleep(0.1)