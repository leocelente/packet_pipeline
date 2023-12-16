from datetime import datetime   
from typing import Callable
from packet import Packet
from plugin_manager import Parser
from position import Position
from typing import Any

class FakeParser(Parser):
    def __init__(self, push: Callable, parameters: dict) -> None:
        super().__init__(push, parameters)

    def parser(self) -> None:
        while not self.done:
            data = self.queue.get()
            pos = Position.random()
            payload = {'snr': -10}
            arrival = datetime.utcnow()
            self.push(Packet(pos, payload, arrival))
        return

        