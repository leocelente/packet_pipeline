from dataclasses import dataclass
from datetime import datetime
from position import Position

@dataclass
class Packet():
    position: Position
    payload: dict
    arrival_time: datetime

    def serializable(self, receiver: dict = {}) -> dict:
        return  {
                'position': self.position.serializable(),
                'payload': self.payload,
                'arrival': self.arrival_time.isoformat() + "Z",
                'receiver': receiver
            }