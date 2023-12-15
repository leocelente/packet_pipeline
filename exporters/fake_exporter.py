from typing import Any
from plugin_manager import Exporter
from gps import GPS

class FakeExporter(Exporter):
    def __init__(self, gps: GPS, params: dict[str, Any]) -> None:
        super().__init__(gps, params)

    def exporter(self) -> None:
        while not self.done:
            packet = self.queue.get()
            my_location = self.gps.current_position()
            print("Fake Exporter", my_location, packet)
        return