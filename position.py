from dataclasses import dataclass
from datetime import datetime
from random import randint


@dataclass
class Position():
    latitude: float
    longitude: float
    altitude: float
    time: datetime

    @staticmethod
    def random():
        lat = -22.5 + (randint(0, 100) / 1000)
        lng = -48 + (randint(0, 100) / 1000)
        alt = 800 + (randint(0, 1000) / 10)
        t = datetime.utcnow()
        return Position(lat, lng, alt, t)

    def serializable(self) -> dict:
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'altitude': self.altitude,
            'time': self.time.isoformat() + "Z"
        }
