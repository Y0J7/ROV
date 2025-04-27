import serial
import time

ser = serial.Serial(
    "COM3",baudrate=115200,timeout=2)
print(f"Connected to {ser.name}")
time.sleep(2)

def send_command(msg):
    print(f"Sending: {msg}")
    ser.write(f"{msg}\r\n".encode())
    ser.flush()
    time.sleep(0.5)
    
    if ser.in_waiting:
        response = ser.readline()
        print(f"Response: {response}")
        print(f"Decoded: {response.decode().strip()}")
    else:
        print("No response")

while True:
    command = input("Enter option on or off or exit: ").strip()
    if command.lower() == "on":
        send_command("1")
    elif command.lower() == "off":
        send_command("0")
    elif command.lower() == "exit":
        break
    else:
        print("Invalid command. Please enter 'on', 'off', or 'exit'.")

ser.close()
print("Serial connection closed")