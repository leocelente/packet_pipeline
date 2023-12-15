from datetime import datetime, timedelta
from typing import Callable, Any
from packet import Packet
from plugin_manager import Parser, ParsingFailure
from position import Position
import pytz

class AlcantaraParser(Parser):
    sample = "85;64;-22.273373;-45.692879;2440.97;\"10:57:10\""
    last_packet: Position
    def __init__(self, push: Callable[[Packet], None], parameters: dict[str, Any]) -> None:
        self.last_packet = Position.random()
        super().__init__(push, parameters)

    def parser(self) -> None:
        while not self.done:
            data = self.queue.get()
            arrival = datetime.utcnow()

            line = data.decode()
            parts = line.split(';')

            if len(parts) < 6:
                continue
            
            rssi = int(parts[0]) * (-1)
            counter = int(parts[1])
            payload = {'rssi': rssi, 'counter': counter}

            latitude = float(parts[2])
            longitude = float(parts[3])
            altitude = float(parts[4])

            time_strs = parts[5].replace('"', '').strip().split(':')
            hour = int(time_strs[0])
            minute = int(time_strs[1])
            second = int(time_strs[2])
            now = datetime.now()
            time = datetime(now.year, now.month, now.day, hour, minute, second) + timedelta(hours=-3)
            # tz = pytz.timezone('America/Sao_Paulo') # should be parameter
            # time = tz.localize(time)
            
            pos = Position(latitude, longitude, altitude, time)
            if pos == self.last_packet:
                continue
            self.last_packet = pos

            self.push(Packet(pos, payload, arrival))
        return

        