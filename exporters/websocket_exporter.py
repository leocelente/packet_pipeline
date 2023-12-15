import asyncio
from typing import Any
import websockets
from plugin_manager import Exporter
from gps import GPS
from threading import Thread
from json import dumps


class WebSocketExporter(Exporter):
    CONNECTIONS: set

    def loop(self):
        while not self.done:
            packet = self.queue.get()
            my_position = self.gps.current_position()
            receiver = {
                'latitude': my_position.latitude,
                'longitude': my_position.longitude,
                'altitude': my_position.altitude,
                'time': my_position.time.isoformat()
            }
            packet_s = dumps(packet.serializable(receiver))
            websockets.broadcast(self.CONNECTIONS, packet_s)

    def __init__(self, gps: GPS, params: dict[str, Any]) -> None:
        super().__init__(gps, params)
        self.CONNECTIONS = set()
        self.broadcast_thread = Thread(target=self.loop, args=(), daemon=True)

    def exporter(self) -> None:
        async def register(websocket):
            self.CONNECTIONS.add(websocket)
            try:
                await websocket.wait_closed()
            finally:
                self.CONNECTIONS.remove(websocket)

        async def main():
            async with websockets.serve(register, "0.0.0.0", 7000):
                self.broadcast_thread.start()
                await asyncio.Future()  # run forever
        asyncio.run(main())
        self.broadcast_thread.join()
        return
