import tkinter as tk
from tkinter import ttk

class ФреймОсновныеДанныеПриказа(ttk.LabelFrame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, width=200, text='_основные_данные_приказа_', style='Custom.TLabelframe', *args, **kwargs)
        self.pack_propagate(False)
        # Здесь можно добавить содержимое левого фрейма
        # self.pack(side=tk.LEFT, fill=tk.Y)  # Не вызываем pack здесь, чтобы управлять из родителя
