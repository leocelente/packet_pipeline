from json import loads

class Config():
    gps: dict
    pipeline: dict
    
    @staticmethod
    def from_file(filename: str):
        contents = ""
        with open(filename, 'r') as file:
            contents = file.read()
        json  = loads(contents)
        config  = Config()
        config.gps = json['gps']
        config.pipeline = json['pipeline']
        return config