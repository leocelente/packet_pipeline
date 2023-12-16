from packet import Packet

class RunningStats():
    packets: list
    successes: dict
    failures: dict
    def __init__(self) -> None:
        self.packets = []
        self.failures = {'parse': 0, 'exporters': {}}
        self.successes = {'parse': 0, 'exporters': {}}

    def register_exporter(self, name: str):
        self.successes['exporters'][name] = 0
        self.failures['exporters'][name] = 0
    
    def parse_fail(self):
        self.failures['parse'] += 1
    def parse_success(self):
        self.successes['parse'] += 1
    
    def exporter_fail(self, name: str):
        self.failures['exporters'][name] += 1

    def exporter_success(self, name: str):
        self.successes['exporters'][name] += 1
    
    def save_packet(self, packet: Packet):
        self.packets.append(packet)

    def get_packets(self) -> list:
        return self.packets
    def get_stats(self):
        return {'success': self.successes, 'failures': self.failures}

stats = RunningStats()
