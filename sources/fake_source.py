from typing import Callable, Any
from plugin_manager import Source
from time import sleep
from random import randint

class FakeSource(Source):
    def __init__(self, push: Callable, parameters: dict) -> None:
        super().__init__(push, parameters)

    def listen(self) -> None:
        while not self.done:
            
            data = bytes([randint(0, 255) for _ in range(128)])
            self.push(data)
            sleep(6)
        return

    def close(self) -> None:
        return super().close()