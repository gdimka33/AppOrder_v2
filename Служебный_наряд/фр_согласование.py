import tkinter as tk
from tkinter import ttk
from виджиты.ви_ПоискОфицера import ПоискОфицера

class ФреймСогласование(tk.Toplevel):
    def __init__(self, master, согласующие=None, callback=None):
        super().__init__(master)
        self.title('Согласование')
        self.resizable(False, True)  # только по вертикали
        self.callback = callback
        self.transient(master)
        self.grab_set()
        self.protocol('WM_DELETE_WINDOW', self._on_cancel)
        self.согласующие = list(согласующие) if согласующие else []
        self._min_width = 400
        self._min_height = 400
        self._build_ui()
        self._refresh_list()
        self._center_window(self._min_width, self._min_height)

    def _center_window(self, width, height):
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)
        self.minsize(width, height)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _build_ui(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.list_frame = ttk.Frame(self.frame)
        self.list_frame.grid(row=0, column=0, columnspan=3, sticky='ew')
        self.frame.grid_columnconfigure(0, weight=1)
        self.add_label = tk.Label(self.frame, text='Добавить', font=("TkDefaultFont", 9, "italic"), fg="#0077cc", cursor="hand2", anchor="w")
        self.add_label.grid(row=1, column=0, sticky='ew', pady=4)
        self.add_label.bind('<Button-1>', self._on_add_label_click)
        self.add_entry = None
        self.btn_ok = ttk.Button(self.frame, text='OK', command=self._on_ok)
        self.btn_ok.grid(row=2, column=0, columnspan=3, sticky='ew', pady=4)

    def _refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        for i, оф in enumerate(self.согласующие):
            фам = оф.get('фамилия', '').capitalize()
            имя = оф.get('имя', '')
            отч = оф.get('отчество', '')
            инициалы = ''
            if имя:
                инициалы += (имя[0] + '.').upper()
            if отч:
                инициалы += (отч[0] + '.').upper()
            звание = оф.get('звание', '')
            отображение = f"{фам} {инициалы}".strip()
            if звание:
                отображение = f"{отображение}, {звание}"
            lbl = tk.Label(self.list_frame, text=отображение, font=("TkDefaultFont", 9, "normal"), anchor="w")
            lbl.grid(row=i, column=0, sticky='ew', pady=1)
            btn_up = tk.Label(self.list_frame, text='↑', fg='#0077cc', cursor='hand2')
            btn_up.grid(row=i, column=1, padx=2)
            btn_up.bind('<Button-1>', lambda e, idx=i: self._on_up(idx))
            btn_down = tk.Label(self.list_frame, text='↓', fg='#0077cc', cursor='hand2')
            btn_down.grid(row=i, column=2, padx=2)
            btn_down.bind('<Button-1>', lambda e, idx=i: self._on_down(idx))
            btn_del = tk.Label(self.list_frame, text='✕', fg='#cc0000', cursor='hand2')
            btn_del.grid(row=i, column=3, padx=2)
            btn_del.bind('<Button-1>', lambda e, idx=i: self._on_delete(idx))
        self.update_idletasks()
        req_height = self.frame.winfo_reqheight() + 40  # запас под отступы и кнопки
        height = max(self._min_height, req_height)
        self.geometry(f'{self._min_width}x{height}')

    def _on_add_label_click(self, event=None):
        if self.add_entry:
            return
        self.add_label.grid_remove()
        self.add_entry_frame = ttk.Frame(self.frame)
        self.add_entry_frame.grid(row=1, column=0, sticky='ew', pady=4)
        поиск = ПоискОфицера(self.add_entry_frame, callback=self._on_add_select)
        поиск.pack(fill=tk.BOTH, expand=True)
        поиск.entry.focus_set()
        self.add_entry = поиск

    def _on_add_select(self, офицер):
        if офицер:
            self.согласующие.append(офицер)
            self._refresh_list()
        if self.add_entry_frame:
            self.add_entry_frame.destroy()
            self.add_entry_frame = None
            self.add_entry = None
        self.add_label.grid(row=1, column=0, sticky='ew', pady=4)

    def _on_delete(self, idx):
        del self.согласующие[idx]
        self._refresh_list()

    def _on_up(self, idx):
        if idx > 0:
            self.согласующие[idx-1], self.согласующие[idx] = self.согласующие[idx], self.согласующие[idx-1]
            self._refresh_list()

    def _on_down(self, idx):
        if idx < len(self.согласующие)-1:
            self.согласующие[idx+1], self.согласующие[idx] = self.согласующие[idx], self.согласующие[idx+1]
            self._refresh_list()

    def _on_ok(self):
        if self.callback:
            self.callback(self.согласующие)
        self.destroy()

    def _on_cancel(self):
        self.destroy()
