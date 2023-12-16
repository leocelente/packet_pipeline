from datetime import datetime   
from typing import Callable
from packet import Packet
from plugin_manager import Parser
from position import Position
from typing import Any
from json import loads

class JSONParser(Parser):
    def __init__(self, push: Callable, parameters: dict) -> None:
        super().__init__(push, parameters)

    def parser(self) -> None:
        while not self.done:
            data = self.queue.get()
            try:
                parsed = loads(data.decode())
                if not "latitude" in parsed:
                    continue
                if not "longitude" in parsed:
                    continue
                if not "latitude" in parsed:
                    continue
                if not "altitude" in parsed:
                    continue
                if not "time" in parsed:
                    continue
                t = datetime.fromisoformat(parsed['time'])
                pos = Position(parsed['latitude'], parsed['longitude'], parsed['altitude'], t)
                arrival = datetime.utcnow()
                payload = {}
                if "payload" in parsed:
                    payload = parsed['payload']
                self.push(Packet(pos, payload, arrival))
                print(pos)
            except:
                continue
        return

        