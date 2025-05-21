import tkinter as tk
from tkinter import ttk

class ФреймСоставНаряда(ttk.LabelFrame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, text='_состав_наряда_', style='Custom.TLabelframe', *args, **kwargs)
        # Здесь можно добавить содержимое правого фрейма
        # self.pack(fill=tk.BOTH, expand=True)  # Не вызываем pack здесь, чтобы управлять из родителя
