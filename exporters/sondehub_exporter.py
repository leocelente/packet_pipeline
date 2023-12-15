from typing import Any
from plugin_manager import Exporter
from gps import GPS
import gzip
import json
import requests
from email.utils import formatdate
from threading import Thread
from time import sleep
from position import Position

SOFTWARE_NAME = 'tccelente'
SOFTWARE_VERSION = '0.0.1'

class SondeHubExporter(Exporter):
    to_send: list[dict]

    position_uploader_thread: Thread
    telemetry_uploader_thread: Thread

    location: Position
    last_location: Position
    
    def __init__(self, gps: GPS, params: dict[str, Any]) -> None:
        super().__init__(gps, params)
        self.to_send = []
        self.last_location = Position.random()
        self.position_uploader_thread = Thread(
            target=self.position_uploader_worker, args=(), daemon=True)
        self.telemetry_uploader_thread = Thread(
            target=self.telemetry_uploader_worker, args=(), daemon=True)
        
        self.position_uploader_thread.start()
        self.telemetry_uploader_thread.start()


    def telemetry_uploader_worker(self) -> None:
        while not self.done:
            sleep(self.parameters['telemetry_upload_interval'])

            if len(self.to_send) == 0:
                continue

            telemetry = json.dumps(self.to_send).encode('utf-8')
            compressed = gzip.compress(telemetry)

            headers = {
                "User-Agent":  f"{SOFTWARE_NAME}-{SOFTWARE_VERSION}",
                "Content-Encoding": "gzip",
                "Content-Type": "application/json",
                "Date": formatdate(timeval=None, localtime=False, usegmt=True)
            }

            req = requests.put(
                'https://api.v2.sondehub.org/sondes/telemetry',
                compressed, timeout=self.parameters['telemetry_upload_interval']/2, headers=headers
            )

            if req.status_code == 200:
                print(f"Sent {len(self.to_send)} frames to SondeHub")
            else:
                print(f"Failed to upload ({req.status_code})  {req.content.decode()}")

            self.to_send.clear()
        return
                
            
    def position_uploader_worker(self) -> None:
        while not self.done:
            sleep(self.parameters['station_upload_interval'])
            self.location = self.gps.current_position()

            position = {
                "software_name": SOFTWARE_NAME,
                "software_version": SOFTWARE_VERSION,
                "uploader_callsign": self.parameters['callsign'],
                "uploader_position": [self.location.latitude, self.location.longitude, self.location.altitude],
                "uploader_antenna": self.parameters['antenna'],
                "uploader_contact_email": self.parameters['email'],
                "mobile": self.parameters['mobile'],
            }

            headers = {
                "User-Agent": f"{SOFTWARE_NAME}-{SOFTWARE_VERSION}",
                "Content-Type": "application/json",
            }
            if self.location == self.last_location:
                continue
            
            req = requests.put(
                'https://api.v2.sondehub.org/listeners',
                json=position,
                timeout=self.parameters['station_upload_interval']/2,
                headers=headers,
            )
            self.last_location = self.location
        return


    def exporter(self) -> None:
        while not self.done:
            packet = self.queue.get()
            payload = packet.payload
            
            if not 'sats' in payload or payload['sats'] < 4:
                continue


            metadata = {
                "software_name": SOFTWARE_NAME,
                "software_version": SOFTWARE_VERSION,
                "uploader_callsign": self.parameters['callsign'],
                "uploader_position": [self.location.latitude, self.location.longitude, self.location.altitude],
                "uploader_antenna": self.parameters['antenna'],
                "time_received": packet.arrival_time.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                "manufacturer": "Vaisala",
            }

            payload['serial'] = payload.pop('id')
            payload = metadata | payload
    
            self.to_send.append(payload)
        return


    def terminate(self):
        self.position_uploader_thread.join(timeout=15)
        self.telemetry_uploader_thread.join(timeout=15)
        return super().terminate()
