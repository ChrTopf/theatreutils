from PyQt5.QtCore import QThread, pyqtSignal
from serial import SerialException

from serial_input.arduino_interface import ArduinoInterface


class GoButtonListener(QThread):
    """Listens to the physical GO button (the Arduino buzzer) on a serial port in the background."""

    pressed = pyqtSignal()
    failed = pyqtSignal(str)

    def __init__(self, port: str, baud_rate: int, parent=None):
        super().__init__(parent)
        self.port = port
        self.baud_rate = baud_rate

    def run(self) -> None:
        try:
            with ArduinoInterface(self.port, self.baud_rate) as arduino:
                while not self.isInterruptionRequested():
                    if arduino.read_index() is not None:
                        self.pressed.emit()
        except (SerialException, OSError, ValueError) as error:
            if not self.isInterruptionRequested():
                self.failed.emit(str(error))

    def stop(self) -> None:
        self.requestInterruption()
        self.wait()
