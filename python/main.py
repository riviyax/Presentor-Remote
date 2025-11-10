import serial
import pyautogui
import time

# Configure your serial port (replace 'COMx' with your actual port)
# On Linux, it might be something like '/dev/ttyACM0'
# On Mac, it might be something like '/dev/tty.usbmodem14201'
# On Windows, it might be something like 'COM3'
ser = serial.Serial('COM3', 9600, timeout=1)  # Adjust COM port and baud rate
time.sleep(2)  # Wait for the serial connection to establish

last_line = ""  # Store the last line received

while True:
    # Read the incoming serial data
    line = ser.readline().decode('utf-8', errors='ignore').strip()  # Read and decode line, ignore errors

    # Check if the data received is "NEXT"
    if line == "NEXT" and line != last_line:  # Only react if it's a new "NEXT"
        print("NEXT detected, typing 'Riviya'...")
        pyautogui.write('Riviya')  # Simulate typing 'Riviya'
        time.sleep(0.5)  # Small delay to avoid sending too many keystrokes
        pyautogui.press('enter')  # Simulate pressing the 'Enter' key
        last_line = line  # Update the last processed line
    elif line != "NEXT":
        last_line = ""  # Reset if a different message is received
