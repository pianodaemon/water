import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "ps")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "hc")))

class CtrlError(Exception):
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

class CtrlModuleError(CtrlError):
    def __init__(self, message = None, module = None):
        super().__init__(message = message)
