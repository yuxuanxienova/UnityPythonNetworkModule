import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from net.MsgBase import MsgBase
class MsgPing(MsgBase):
    def __init__(self):
        super().__init__()
        self.protoName = "MsgPing"

class MsgPong(MsgBase):
    def __init__(self):
        super().__init__()
        self.protoName = "MsgPong"
class MyMessage(MsgBase):
    def __init__(self):
        super().__init__()
        self.protoName = "MyMessage"
        self.content = ""