# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from справочники import СПРАВОЧНИК_ОФИЦЕРОВ, СПРАВОЧНИК_ЗВАНИЙ, СПРАВОЧНИК_ДОЛЖНОСТЕЙ, СПРАВОЧНИК_ПОДРАЗДЕЛЕНИЙ
from logger import logger

class ПоискОфицера(ttk.Frame):
    """
    Виджет для поиска офицеров.
    Состоит из поля ввода и выпадающего списка результатов.
    """
    def __init__(self, родитель, callback=None, placeholder="Введите фамилию офицера для поиска...", высота_списка=5):
        super().__init__(родитель)
        
        self.callback = callback
        self.placeholder = placeholder
        self.результаты_поиска = []
        self.высота_списка = высота_списка
        self.root = родитель
        self.search_timer = None
        self.выбранный_офицер = None
        
        # Создаем поле ввода
        self.entry = ttk.Entry(self)
        self.entry.pack(fill='x')
        self.entry.insert(0, self.placeholder)
        self.entry.config(foreground='gray')
        
        # Создаем выпадающее окно
        self.popup = None
        self.список = None
        
        # Привязываем обработчики событий
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        self.entry.bind("<KeyRelease>", self._on_key_release)
        self.entry.bind("<Return>", self._on_return)
        self.entry.bind("<Escape>", self._on_escape)
        self._bind_click_outside()

    def _создать_список(self):
        if self.popup:
            self.popup.destroy()
            
        self.popup = tk.Toplevel(self)
        self.popup.overrideredirect(True)
        self.popup.transient()
        
        frame = ttk.Frame(self.popup)
        frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        self.список = tk.Listbox(
            frame,
            height=self.высота_списка,
            activestyle='none',
            selectmode="single",
            relief='flat',
            borderwidth=0,
            highlightthickness=1,
            background='white',
            selectbackground='#E8E8E8',
            selectforeground='black',
            highlightbackground='#ADD8E6',
            highlightcolor='#ADD8E6'
        )
        self.список.pack(fill="both", expand=True)
        
        self.список.bind("<Motion>", self._on_mouse_motion)
        self.список.bind("<Button-1>", self._on_click_item)
        self.popup.bind("<FocusOut>", self._on_popup_focus_out)
        
    def _выполнить_поиск(self, текст_поиска):
        try:
            текст_поиска = текст_поиска.lower()
            self.результаты_поиска = []
            
            if not self.popup or not self.список:
                self._создать_список()
            self.список.delete(0, tk.END)
            
            for оф in СПРАВОЧНИК_ОФИЦЕРОВ:
                фам = оф.get('фамилия', '').lower()
                имя = оф.get('имя', '').lower()
                отч = оф.get('отчество', '').lower() if оф.get('отчество') else ''
                
                if (текст_поиска in фам) or (текст_поиска in имя) or (текст_поиска in отч):
                    офицер = self._форматировать_офицера(оф)
                    self.результаты_поиска.append(офицер)
                    self.список.insert(tk.END, офицер['отображение'])
            
            if self.результаты_поиска:
                self._показать_список()
            else:
                self._скрыть_список()
                
        except Exception as e:
            logger.error(f"Ошибка при поиске офицеров: {e}")
            self._скрыть_список()

    def _форматировать_офицера(self, оф):
        фамилия = оф['фамилия'].capitalize()
        имя = оф['имя']
        отчество = оф['отчество'] if оф['отчество'] else ''
        инициалы = ''
        if имя:
            инициалы += (имя[0] + '.').upper()
        if отчество:
            инициалы += (отчество[0] + '.').upper()
        фио = f"{фамилия} {инициалы}".strip()
        звание = ''
        сокращение = ''
        if оф.get('звание_id'):
            звание_row = next((z for z in СПРАВОЧНИК_ЗВАНИЙ if z['id'] == оф['звание_id']), None)
            if звание_row:
                звание = звание_row['наименование'].capitalize()
                сокращение = звание_row.get('сокращение', '')
        подразделение = ''
        if оф.get('подразделение_id'):
            подразделение_row = next((p for p in СПРАВОЧНИК_ПОДРАЗДЕЛЕНИЙ if p['id'] == оф['подразделение_id']), None)
            if подразделение_row:
                подразделение = подразделение_row['наименование']
        должность = ''
        if оф.get('должность_id'):
            должность_row = next((d for d in СПРАВОЧНИК_ДОЛЖНОСТЕЙ if d['id'] == оф['должность_id']), None)
            if должность_row:
                должность = должность_row['наименование'].capitalize()
        # Формируем строку: ФИО, звание (сокр.), подразделение, должность
        parts = [фио]
        if сокращение:
            parts.append(сокращение)
        elif звание:
            parts.append(звание)
        if подразделение:
            parts.append(подразделение)
        if должность:
            parts.append(должность)
        отображение = ', '.join([p for p in parts if p])
        return {
            'id': оф['id'],
            'отображение': отображение,
            'фамилия': фамилия,
            'имя': имя,
            'отчество': отчество,
            'звание': звание,
            'сокращение': сокращение,
            'должность': должность,
            'подразделение': подразделение
        }

    def _показать_список(self):
        if self.popup and self.список.size() > 0:
            import tkinter.font as tkFont
            font = tkFont.Font(font=self.список.cget("font"))
            max_width = 120  # минимальная ширина
            for i in range(self.список.size()):
                text = self.список.get(i)
                w = font.measure(text) + 30  # небольшой запас
                if w > max_width:
                    max_width = w
            max_width = min(max_width, 900)  # ограничение максимальной ширины
            x = self.entry.winfo_rootx()
            y = self.entry.winfo_rooty() + self.entry.winfo_height()
            self.popup.geometry(f"{max_width}x{self.список.winfo_reqheight()}+{x}+{y}")
            self.popup.deiconify()
            self.popup.lift()

    def _скрыть_список(self, event=None):
        if self.popup:
            self.popup.withdraw()

    def _on_mouse_motion(self, event):
        self.список.selection_clear(0, tk.END)
        self.список.selection_set(self.список.nearest(event.y))

    def _on_click_item(self, event):
        if self.список and self.список.curselection():
            self._выбрать_элемент()

    def _выбрать_элемент(self):
        if not self.список or not self.список.curselection():
            return
            
        индекс = self.список.curselection()[0]
        if 0 <= индекс < len(self.результаты_поиска):
            self.выбранный_офицер = self.результаты_поиска[индекс]
            self.установить_значение(self.выбранный_офицер)
            self._скрыть_список()
            if self.callback:
                self.callback(self.выбранный_офицер)

    def _on_popup_focus_out(self, event):
        if self.focus_get() != self.entry:
            self._скрыть_список()

    def _on_focus_in(self, event):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(foreground='black')

    def _on_focus_out(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(foreground='gray')

    def _on_key_release(self, event):
        if event.keysym in ('Up', 'Down', 'Left', 'Right', 'Shift_L', 'Shift_R', 'Control_L', 'Control_R'):
            return
            
        if self.search_timer:
            self.after_cancel(self.search_timer)
            
        текст = self.entry.get().strip()
        if текст and текст != self.placeholder:
            self.search_timer = self.after(300, lambda: self._выполнить_поиск(текст))
        else:
            self._скрыть_список()

    def _on_return(self, event):
        if self.popup and self.popup.winfo_viewable():
            self._выбрать_элемент()
            return "break"
        return None

    def _on_escape(self, event=None):
        self.очистить()
        self.entry.selection_clear()
        self.entry.icursor(0)
        self.entry.event_generate('<FocusOut>')
        self.entry.master.focus_set()
        return "break"

    def _bind_click_outside(self):
        def on_click(event):
            widget = event.widget
            # Если клик вне entry и вне popup
            if not (widget is self.entry or (self.popup and str(widget).startswith(str(self.popup)))):
                self.очистить()
                self.entry.event_generate('<FocusOut>')
                self.entry.master.focus_set()
        self.entry.bind_all('<Button-1>', on_click, add='+')

    def очистить(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.placeholder)
        self.entry.config(foreground='gray')
        self._скрыть_список()
        self.результаты_поиска = []
        self.выбранный_офицер = None

    def установить_значение(self, офицер):
        if офицер:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, офицер['отображение'])
            self.entry.config(foreground='black')
            if офицер not in self.результаты_поиска:
                self.результаты_поиска.append(офицер)
            self.выбранный_офицер = офицер
            return True
        return False

    def получить_значение(self):
        return self.выбранный_офицер

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Тест поиска офицера")
    root.geometry("400x200")
    
    def on_select(офицер):
        print(f"Выбран офицер: {офицер['отображение']}")
        
    поиск = ПоискОфицера(root, callback=on_select)
    поиск.pack(pady=20)
    
    root.mainloop()
