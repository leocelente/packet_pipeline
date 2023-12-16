from datetime import datetime
from json import dumps
from typing import Any
from plugin_manager import Exporter
from gps import GPS


class CSVExporter(Exporter):
    filename: str

    def __init__(self, gps: GPS, params: dict) -> None:
        super().__init__(gps, params)
        now = datetime.utcnow()
        self.filename = f"data_{now.strftime('%Y-%m-%d-%H-%M-%S')}.csv"
        with open(self.filename, 'w+') as file:
            file.write("time, lat, lng, alt, payload\r\n")

    def exporter(self) -> None:
        while not self.done:
            packet = self.queue.get()
            position = packet.position
            with open(self.filename, 'a+') as file:
                file.write(f"{position.time.isoformat()}, {position.latitude}, {position.longitude}, {position.altitude}, '{dumps(packet.payload)}'\r\n")
        return
