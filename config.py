from json import loads
from dataclasses import dataclass

@dataclass
class Config():
    gps: dict
    pipeline: dict
    
    @staticmethod
    def from_file(filename: str):
        contents = ""
        with open(filename, 'r') as file:
            contents = file.read()
        json  = loads(contents)
        config  = Config(json['gps'], json['pipeline'])
        return config