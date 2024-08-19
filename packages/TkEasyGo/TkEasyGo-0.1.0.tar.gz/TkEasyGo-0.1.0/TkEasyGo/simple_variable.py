import tkinter as tk


class SimpleVariable:
    """A simple wrapper around Tkinter's StringVar with additional utility methods."""
    def __init__(self, initial_value=None):
        self.var = tk.StringVar(value=initial_value)
    
    def get(self):
        return self.var.get()
    
    def set(self, value):
        self.var.set(value)
    
    def trace(self, callback):
        self.var.trace_add("write", lambda *args: callback(self.var.get()))