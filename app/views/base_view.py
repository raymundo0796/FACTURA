
from tkinter import ttk


class BaseView(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        """Método para configurar la interfaz de usuario"""
        pass