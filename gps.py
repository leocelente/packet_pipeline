from position import Position
from config import Config
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
from threading import Thread
from gpsdclient import GPSDClient

class GPS(ABC):
    @abstractmethod
    def current_position(self) -> Position:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

class GPS_Static(GPS):
    position: Position
    def __init__(self, param: dict[str, Any]) -> None:
        time = datetime.utcnow()
        self.position = Position(param["latitude"], param["longitude"], param["altitude"], time)
        super().__init__()

    def current_position(self) -> Position:
        return self.position

    def close(self) -> None:
        return super().close()
    


class GPS_GPSD(GPS):
    gpsd_thread: Thread
    current: Position
    done: bool
    param: dict
    def gpsd_worker(self):
        with GPSDClient() as client:
            while not self.done:    
                for result in client.dict_stream(convert_datetime=True, filter=["TPV"]):
                    lat = result.get("lat", self.param["latitude"])
                    lon = result.get("lon", self.param["longitude"])
                    alt = result.get("alt", self.param["altitude"])
                    t = result.get('time', datetime.now().utcnow())
                    pos = Position(lat, lon, alt, t)
                    self.current = pos


    def __init__(self, param: dict[str, Any]) -> None:
        super().__init__()

        time = datetime.utcnow()
        self.current = Position(param["latitude"], param["longitude"], param["altitude"], time)
        self.param = param
        self.done = False
        self.gpsd_thread = Thread(target=self.gpsd_worker, args=(), daemon=True)
        self.gpsd_thread.start()
    
    def terminate(self):
        self.done = True

    def close(self) -> None:
        self.terminate()
        self.gpsd_thread.join(timeout=15)
        return super().close()

    def current_position(self) -> Position:
        return self.current
        

class GPS_Factory():
    gps: GPS
    def __init__(self, config: Config) -> None:
        if config.gps['type'] == 'static':
            self.gps = GPS_Static(config.gps['parameters'])
        else:
            self.gps = GPS_GPSD(config.gps['parameters'])

    def get_gps(self) -> GPS:
        return self.gps


global_gps = object()