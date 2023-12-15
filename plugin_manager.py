from abc import ABC, abstractmethod
from typing import Callable
from os.path import dirname
from os import listdir
from importlib import import_module
from inspect import isclass
from packet import Packet
import gps as gps_module
from queue import Queue
from typing import Any

class SourceFailure(Exception):
    def __init__(self, message: str = "Problem with data source") -> None:
        self.message = message
        super().__init__(self.message)

class Source(ABC):
    done: bool
    push: Callable[[bytes], None]
    parameters: dict[str, Any]
    def __init__(self, push: Callable[[bytes], None], parameters: dict[str, Any]) -> None:
        super().__init__()
        self.done = False 
        self.push = push 
        self.parameters = parameters

    @abstractmethod
    def listen(self) -> None:
        pass

    def terminate(self):
        self.done = True

    @abstractmethod
    def close(self) -> None:
        pass



class ParsingFailure(Exception):
    def __init__(self, data: bytes, message: str = "Couldn't parse data to packet") -> None:
        self.data = data
        self.message = message
        super().__init__(self.data, self.message)

class Parser(ABC):
  done: bool
  queue: Queue[bytes]
  push: Callable[[Packet], None]
  parameters: dict[str, Any]
  def __init__(self, push: Callable[[Packet], None], parameters: dict[str, Any]) -> None:
      self.done = False
      self.queue = Queue(16)
      self.push = push 
      self.parameters = parameters
      super().__init__()
  
  @abstractmethod
  def parser(self) -> None:
      pass

  def terminate(self):
      self.done = True



class ExportFailure(Exception):
    def __init__(self, packet: Packet, message: str = "Couldn't export packet") -> None:
        self.packet = packet
        self.message = message
        super().__init__(self.packet, self.message)

class Exporter(ABC):
  done: bool
  gps: gps_module.GPS
  queue: Queue[Packet]
  parameters: dict[str, Any]
  def __init__(self, gps: gps_module.GPS, params: dict[str, Any]) -> None:
      self.done = False
      self.gps = gps
      self.queue = Queue(32)
      self.parameters = params
      super().__init__()
  
  @abstractmethod
  def exporter(self) -> None:
      pass

  def terminate(self):
      self.done = True



class PluginFailure(Exception):
    def __init__(self, module) -> None:
        self.module = module
        super().__init__(self.module)

class PluginManager():
    modules = {'sources': {}, 'parsers':{}, 'exporters':{}}
    def __init__(self) -> None:
        path = dirname(__file__)        
        directories = ['sources', 'parsers', 'exporters']
        modules_names = []
        for directory in directories:
            files = listdir(path + '/' + directory)
            files.sort()
            for file in files:
                if not file.endswith('.py'):
                    continue

                module_name = file.split('.')[0]
                modules_names.append(f"{directory}.{module_name}")
            
        for name in modules_names:
            try:
                module = import_module(name)
                attributes = dir(module)
                for attribute in attributes:
                    symbol = getattr(module, attribute)
                    if not isclass(symbol):
                        continue
                    if symbol in [Source, Parser, Exporter]:
                        continue
                    if issubclass(symbol, Parser):
                        self.modules['parsers'][attribute] = symbol
                    elif issubclass(symbol, Exporter):
                        self.modules['exporters'][attribute] = symbol
                    elif issubclass(symbol, Source):
                        self.modules['sources'][attribute] = symbol
                    else:
                        pass
            except ModuleNotFoundError:
                raise PluginFailure(name)

        
    def get_plugins(self):
        return self.modules

