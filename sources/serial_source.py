from typing import Callable, Any
from plugin_manager import Source
from serial import Serial

class SerialSource(Source):
    port: Serial
    def __init__(self, push: Callable, parameters: dict) -> None:
        super().__init__(push, parameters)
        self.serial = Serial(self.parameters['port'], baudrate=self.parameters['baudrate'])

    def listen(self) -> None:
        while not self.done:
            data = self.serial.read_until()
            self.push(data)
        return

    def close(self) -> None:
        self.serial.close()
        return super().close()