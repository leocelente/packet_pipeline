from plugin_manager import Exporter
import gps
from queue import Queue
from packet import Packet
from threading import Thread
import running_stats
from typing import Any

class ExporterManager():
    exporters: list 
    threads: list
    
    def __init__(self, exporters: list) -> None:
        self.exporters = []
        self.threads = []
        for (classname, params)  in exporters:
            self.exporters.append(classname(gps.global_gps, params))
        for exporter in self.exporters:
            thread = Thread(target=exporter.exporter, args=(), daemon=True)
            self.threads.append(thread)
        for thread in self.threads:
            thread.start()

    def push(self, packet: Packet):
        running_stats.stats.save_packet(packet)
        for exporter in self.exporters:
            exporter.queue.put(packet)

    def close(self):
        for exporter in self.exporters:
            exporter.terminate()

        for thread in self.threads:
            thread.join(timeout=15)
        