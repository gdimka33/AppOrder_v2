import tkinter as tk
from tkinter import ttk
from datetime import date
from tkcalendar import DateEntry
from виджиты.ви_ПоискОфицера import ПоискОфицера

class ФреймОсновныеДанныеПриказа(ttk.LabelFrame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, text='_основные_данные_приказа_', style='Custom.TLabelframe', *args, **kwargs)
        self.configure(width=400, height=320)
        self.pack_propagate(False)
        self.grid_propagate(False)

        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.content_frame.grid_propagate(False)
        self.content_frame.grid_columnconfigure(1, minsize=220, weight=0)

        # Дата создания
        ttk.Label(self.content_frame, text="Дата создания:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.дата_создания = DateEntry(self.content_frame, date_pattern='yyyy-mm-dd', width=15)
        self.дата_создания.set_date(date.today())
        self.дата_создания.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        # Дата регистрации
        ttk.Label(self.content_frame, text="Дата регистрации:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.дата_регистрации = DateEntry(self.content_frame, date_pattern='yyyy-mm-dd', width=15)
        self.дата_регистрации.set_date(date.today())
        self.дата_регистрации.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        # Номер приказа
        ttk.Label(self.content_frame, text="Номер приказа:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.номер_приказа = ttk.Entry(self.content_frame)
        self.номер_приказа.insert(0, "000")
        self.номер_приказа.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        # Исполнитель
        ttk.Label(self.content_frame, text="Исполнитель:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.исполнитель = tk.Label(
            self.content_frame,
            text="Выбрать",
            font=("TkDefaultFont", 9, "italic"),
            cursor="hand2",
            bd=1,
            padx=8,
            pady=2,
            width=30,
            anchor="w"
        )
        self.исполнитель.grid(row=3, column=1, sticky="ew", padx=5, pady=2)
        self.исполнитель.bind("<Button-1>", self._on_lbl_click)

        # Руководитель
        ttk.Label(self.content_frame, text="Руководитель:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.руководитель = tk.Label(
            self.content_frame,
            text="Выбрать",
            font=("TkDefaultFont", 9, "italic"),
            cursor="hand2",
            bd=1,
            padx=8,
            pady=2,
            width=30,
            anchor="w"
        )
        self.руководитель.grid(row=4, column=1, sticky="ew", padx=5, pady=2)
        self.руководитель.bind("<Button-1>", self._on_ruk_click)

        # Контроль
        ttk.Label(self.content_frame, text="Контроль:").grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.контроль = tk.Label(
            self.content_frame,
            text="Выбрать",
            font=("TkDefaultFont", 9, "italic"),
            cursor="hand2",
            bd=1,
            padx=8,
            pady=2,
            width=30,
            anchor="w"
        )
        self.контроль.grid(row=5, column=1, sticky="ew", padx=5, pady=2)
        self.контроль.bind("<Button-1>", self._on_kontrol_click)

        # Согласование
        ttk.Label(self.content_frame, text="Согласование:").grid(row=6, column=0, sticky="w", padx=5, pady=2)
        # Здесь будет размещен фрейм согласования

        # Пустые фреймы для фиксированной высоты строк
        for i in range(7):
            spacer = tk.Frame(self.content_frame, height=30)
            spacer.grid(row=i, column=2)

    def _on_lbl_click(self, event):
        self._show_search_widget(self.исполнитель, 3)

    def _on_ruk_click(self, event):
        self._show_search_widget(self.руководитель, 4)

    def _on_kontrol_click(self, event):
        self._show_search_widget(self.контроль, 5)

    def _show_search_widget(self, label_widget, row):
        def on_select(офицер):
            if офицер:
                фамилия = офицер.get('фамилия', '').capitalize()
                имя = офицер.get('имя', '')
                отчество = офицер.get('отчество', '')
                инициалы = ''
                if имя:
                    инициалы += (имя[0] + '.').upper()
                if отчество:
                    инициалы += (отчество[0] + '.').upper()
                звание = офицер.get('звание', '')
                отображение = f"{фамилия} {инициалы}".strip()
                if звание:
                    отображение = f"{отображение}, {звание}"
                отображение = ' '.join(отображение.split())
                макс_длина = 40
                if len(отображение) > макс_длина:
                    отображение = отображение[:макс_длина-3] + '...'
                label_widget.configure(text=отображение, font=("TkDefaultFont", 9, "normal"))
                tooltip_text = self._get_full_officer_info(офицер)
                self._add_tooltip(label_widget, tooltip_text)
            if поиск.winfo_exists():
                поиск.destroy()
            label_widget.grid()

        label_widget.grid_remove()
        поиск = ПоискОфицера(self.content_frame)
        поиск.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
        поиск.callback = on_select
        поиск.entry.focus_set()

        def on_click_outside(event):
            widget = event.widget
            if widget not in (поиск, поиск.entry, getattr(поиск, 'список', None)):
                выбранный = поиск.получить_значение()
                if выбранный:
                    on_select(выбранный)
                elif поиск.winfo_exists():
                    поиск.destroy()
                    label_widget.grid()

        def on_focus_out(event):
            self.after(200, lambda: on_click_outside(event))

        поиск.bind_all('<Button-1>', on_click_outside, add='+')
        поиск.entry.bind('<FocusOut>', on_focus_out)

    def _get_full_officer_info(self, офицер):
        # Формирует строку для tooltip
        звание = офицер.get('звание', '')
        фамилия = офицер.get('фамилия', '').capitalize()
        имя = офицер.get('имя', '').capitalize()
        отчество = офицер.get('отчество', '').capitalize()
        должность = офицер.get('должность', '')
        подразделение = офицер.get('подразделение', '')
        fio_full = f"{фамилия} {имя} {отчество}".strip()
        parts = []
        if звание:
            parts.append(звание)
        if fio_full:
            parts.append(fio_full)
        if должность:
            parts.append(f"Должность: {должность}")
        if подразделение:
            parts.append(f"Подразделение: {подразделение}")
        return '\n'.join(parts)

    def _add_tooltip(self, widget, text):
        # Удаляем старый tooltip, если был
        if hasattr(widget, '_tooltip_window') and widget._tooltip_window:
            widget._tooltip_window.destroy()
            widget._tooltip_window = None
        def show_tooltip(event):
            if hasattr(widget, '_tooltip_window') and widget._tooltip_window:
                return
            x = widget.winfo_rootx() + 20
            y = widget.winfo_rooty() + widget.winfo_height() + 5
            tw = tk.Toplevel(widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")
            label = tk.Label(tw, text=text, justify='left', background='#ffffe0', relief='solid', borderwidth=1, font=("TkDefaultFont", 9))
            label.pack(ipadx=4, ipady=2)
            widget._tooltip_window = tw
        def hide_tooltip(event):
            if hasattr(widget, '_tooltip_window') and widget._tooltip_window:
                widget._tooltip_window.destroy()
                widget._tooltip_window = None
        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)
        widget._tooltip_window = None
