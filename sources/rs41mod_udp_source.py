from typing import Callable, Any
from plugin_manager import Source
from subprocess import Popen, PIPE, STDOUT, list2cmdline
from shlex import shlex

CMD_FULL = "nc -ul -p 4030 | rs41mod --json --IQ 0.0 - 48000 32"


class RS41UDPSource(Source):
    netcat_process: Popen
    rs41mod_process: Popen

    def __init__(self, push: Callable, parameters: dict) -> None:
        super().__init__(push, parameters)

        programs = CMD_FULL.split(' | ')
        netcat_cmd = list(shlex(programs[0], punctuation_chars=True))

        if 'netcat_path' in self.parameters:
            netcat_cmd[0] = str(self.parameters['netcat_path'])

        port = str(self.parameters['port'])
        netcat_cmd[-1] = port

        rs41mod_cmd = list(shlex(programs[1], punctuation_chars=True))
        if 'rs41mod_path' in self.parameters:
            rs41mod_cmd[0] = str(self.parameters['rs41mod_path'])

        self.netcat_process = Popen(netcat_cmd, stdout=PIPE, stderr=PIPE, stdin=None)
        self.rs41mod_process = Popen(rs41mod_cmd,stdout=PIPE, stderr=PIPE, stdin=self.netcat_process.stdout)

    def listen(self) -> None:
        for line in iter(self.rs41mod_process.stdout.readline, b''):
            print("Decoding RS41 packets")
            self.push(line)
        return

    def close(self) -> None:
        self.netcat_process.terminate()
        self.rs41mod_process.terminate()
        return super().close()
