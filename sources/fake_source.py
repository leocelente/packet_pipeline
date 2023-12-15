from typing import Callable, Any
from plugin_manager import Source
from time import sleep
from random import randbytes

class FakeSource(Source):
    def __init__(self, push: Callable[[bytes], None], parameters: dict[str, Any]) -> None:
        super().__init__(push, parameters)

    def listen(self) -> None:
        while not self.done:
            data = randbytes(128)
            self.push(data)
            sleep(6)
        return

    def close(self) -> None:
        return super().close()