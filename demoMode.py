import RPi.GPIO as GPIO
import time
import serial
import glob
import os

# Set up GPIO for the button
BUTTON_PIN = 17  # Adjust the GPIO pin according to your setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up serial communication
def find_arduino_port():
    ports = glob.glob('/dev/tty[A-Za-z]*')
    for port in ports:
        try:
            with serial.Serial(port) as ser:
                ser.write(b'ping')  # Send a test command
                response = ser.readline().decode().strip()
                if response == 'pong':
                    return port
        except serial.SerialException:
            pass
    return None

arduino_port = find_arduino_port()

def send_serial_command(command):
    if arduino_port:
        with serial.Serial(arduino_port, 9600, timeout=1) as ser:
            ser.write(command.encode())
        print(f"Sent command to Arduino: {command}")
    else:
        print("Arduino not found.")

# Play audio function using mpg321 command
def play_audio(file_path):
    os.system(f'mpg321 {file_path}')

# Main loop
try:
    while True:
        button_state = GPIO.input(BUTTON_PIN)
        
        if button_state == GPIO.HIGH:
            print("Button Pressed!")

            # Replace 'your_audio_file.mp3' with the actual path to your MP3 file
            audio_file_path = 'resources/speech.mp3'

            # Play the audio file using mpg321
            play_audio(audio_file_path)

            # Send serial command to Arduino
            send_serial_command('m')

            time.sleep(1)  # Debounce delay

except KeyboardInterrupt:
    GPIO.cleanup()
