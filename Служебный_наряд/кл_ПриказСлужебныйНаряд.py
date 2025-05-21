import tkinter as tk
from tkinter import ttk
from .фр_основные_данные_приказа import ФреймОсновныеДанныеПриказа
from .фр_состав_наряда import ФреймСоставНаряда

class ПриказСлужебныйНаряд(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pack(fill=tk.BOTH, expand=True)
        self._создать_фреймы()

    def _создать_фреймы(self):
        # Левый фрейм вынесен в отдельный класс
        self.фрейм_основные_данные_приказа = ФреймОсновныеДанныеПриказа(self)
        self.фрейм_основные_данные_приказа.pack(side=tk.LEFT, fill=tk.Y)

        # Правый фрейм вынесен в отдельный класс
        self.фрейм_состав_наряда = ФреймСоставНаряда(self)
        self.фрейм_состав_наряда.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)