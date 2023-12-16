from json import loads
from socketserver import  BaseServer
from typing import Callable, Any
from plugin_manager import Source
from http.server import BaseHTTPRequestHandler, HTTPServer

def ServerFactory(push: Callable):
    class Server(BaseHTTPRequestHandler):
        def __init__(self, request, client_address, server: BaseServer) -> None:
            super().__init__(request, client_address, server)
        def do_POST(self):
            length = self.headers['content-length']
            data = self.rfile.read(int(length))
            push(data)
            self.send_response(200, 'OK')
    return Server


class HttpSource(Source):
    webServer: HTTPServer
    def __init__(self, push: Callable, parameters: dict) -> None:
        super().__init__(push, parameters)
        self.webServer = HTTPServer(("0.0.0.0", 4567), ServerFactory(push))

    def listen(self) -> None:
        while not self.done:        
            self.webServer.serve_forever()
        return

    def close(self) -> None:
        self.webServer.server_close()
        return super().close()