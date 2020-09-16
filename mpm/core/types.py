from typing import List, Any, Union
from plumbum.machines import LocalMachine, SshMachine
from plumbum.machines.paramiko_machine import ParamikoMachine

Machine = Union[LocalMachine, SshMachine, ParamikoMachine]
