from plugin_manager import PluginManager
from exporter_manager import ExporterManager
from config import Config
from plugin_manager import Source, Parser, Exporter
from queue import Queue
from threading import Thread

class PipeLine():
    source: Source
    data_queue: Queue
    parser: Parser
    export_manager: ExporterManager
    plugin_manager: PluginManager
    
    def __init__(self, config: Config) -> None:
        self.plugin_manager = PluginManager()
        blocks = self.plugin_manager.get_plugins()
        SelectedSource = blocks['sources'][config.pipeline['source']['name']]
        SelectedParser = blocks['parsers'][config.pipeline['parser']['name']]

        SelectedExporters = []
        for wanted_exporter in config.pipeline['exporters']:
            found = blocks['exporters'][wanted_exporter['name']] 
            SelectedExporters.append((found, wanted_exporter['parameters'])) 
            
        self.export_manager = ExporterManager(SelectedExporters)
        self.parser: Parser = SelectedParser(self.export_manager.push, config.pipeline['parser']['parameters'])
        self.parser_thread = Thread(target=self.parser.parser, args=(), daemon=True)
        self.parser_thread.start()

        self.source: Source = SelectedSource(self.parser.queue.put, config.pipeline['source']['parameters'])
        self.source_thread = Thread(target=self.source.listen, args=(), daemon=True)
        self.source_thread.start()

    def close(self):
        self.source.terminate()
        self.source_thread.join(timeout=30)
        self.parser.terminate()
        self.parser_thread.join(timeout=30)
        self.export_manager.close()

    