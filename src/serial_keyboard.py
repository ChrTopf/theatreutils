import sys
import time
import pynput.keyboard

def find_arduino_port():
    import serial.tools.list_ports

    ports = serial.tools.list_ports.comports()

    for port in ports:
        if 'Arduino' in port.description or 'USB' in port.description:
            return port.device

    return None

def main():
    port = find_arduino_port()

    if not port:
        print("Arduino not found. Please specify the port manually:")
        print("Available ports:")
        import serial.tools.list_ports
        for port_info in serial.tools.list_ports.comports():
            print(f"  {port_info.device}: {port_info.description}")

        port = input("Enter port (e.g., /dev/ttyUSB0 or COM3): ").strip()

    print(f"Connecting to Arduino on {port}...")

    try:
        ser = serial.Serial(port, 9600, timeout=1)
        time.sleep(2)

        print("Connected! Listening for key presses...")
        print("Press Ctrl+C to exit")

        keyboard = pynput.keyboard.Controller()

        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()

                if line.startswith("KEY:"):
                    key_char = line[4:]
                    print(f"Received key: '{key_char}'")

                    try:
                        keyboard.press(key_char)
                        keyboard.release(key_char)
                        print(f"Pressed: '{key_char}'")
                    except Exception as e:
                        print(f"Error pressing key '{key_char}': {e}")

            time.sleep(0.01)

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        if 'ser' in locals():
            ser.close()
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()