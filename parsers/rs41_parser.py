from datetime import datetime   
from typing import Callable
from packet import Packet
from plugin_manager import Parser
from position import Position
from typing import Any
from json import loads

class RS41Parser(Parser):
    def __init__(self, push: Callable[[Packet], None], parameters: dict[str, Any]) -> None:
        super().__init__(push, parameters)

    def parser(self) -> None:
        while not self.done:
            data = self.queue.get()
            try:
                parsed = loads(data.decode())
                if not "lat" in parsed:
                    continue
                if not "lon" in parsed:
                    continue
                if not "alt" in parsed:
                    continue
                if not "datetime" in parsed:
                    continue
                if not 'sats' in parsed:
                    continue

                if self.parameters['require_gps_lock'] and parsed['sats'] < 4:
                    print("no lock", parsed['sats'])
                    continue

                print("RS41 Parser got a packet")
            
                t = datetime.fromisoformat(parsed['datetime'].replace('Z', ''))
                pos = Position(parsed['lat'], parsed['lon'], parsed['alt'], t)
                arrival = datetime.utcnow()
                payload = parsed
                self.push(Packet(pos, payload, arrival))
            except:
                continue
        return

        