import tkinter as tk
from tkinter import ttk
from справочники import СПРАВОЧНИК_ЗВАНИЙ

class ВиджетЗвания(ttk.Combobox):
    def __init__(self, родитель, категория=None, **kwargs):
        kwargs.setdefault('state', 'readonly')
        kwargs.setdefault('width', 20)
        if категория:
            значения = [z['наименование'] for z in СПРАВОЧНИК_ЗВАНИЙ if z['категория'] in (категория, 'общее')]
        else:
            значения = [z['наименование'] for z in СПРАВОЧНИК_ЗВАНИЙ]
        kwargs['values'] = значения
        super().__init__(родитель, **kwargs)
        if значения:
            self.current(0)
    def get_id(self):
        текущее_значение = self.get()
        for z in СПРАВОЧНИК_ЗВАНИЙ:
            if z['наименование'] == текущее_значение:
                return z['id']
        return None
    def set_by_id(self, id_звания):
        for i, z in enumerate(СПРАВОЧНИК_ЗВАНИЙ):
            if z['id'] == id_звания:
                self.current(i)
                return True
        return False
