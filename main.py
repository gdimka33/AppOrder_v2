import tkinter as tk
from tkinter import ttk
from logger import logger
from стили import СтилиПриложения
from PIL import Image, ImageTk
import os
from Служебный_наряд.кл_ПриказСлужебныйНаряд import ПриказСлужебныйНаряд

logger.info('Приложение запущено')

class ИндикаторСостояния(tk.Canvas):
    def __init__(self, parent, size=16):
        super().__init__(parent, width=size, height=size, bg='#f0f0f0', highlightthickness=0)
        self.size = size
        
        # Загружаем иконку редактирования
        icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'file-edit.png')
        self.edit_icon = Image.open(icon_path)
        self.edit_icon = self.edit_icon.resize((size-4, size-4), Image.Resampling.LANCZOS)
        self.edit_icon_tk = ImageTk.PhotoImage(self.edit_icon)
        
        self.очистить()

    def установить_состояние(self, состояние):
        self.delete("all")
        padding = 2
        if состояние == "не_начато":
            pass  # пустой индикатор
        elif состояние == "в_процессе":
            self.create_image(self.size/2, self.size/2, image=self.edit_icon_tk)
        elif состояние == "завершено":
            self.create_oval(padding, padding, self.size-padding, self.size-padding, fill="green")

    def очистить(self):
        self.delete("all")

class ГлавноеОкно(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Учёт личного состава")
        self.state('zoomed')

        # Инициализируем стили
        self.стили = СтилиПриложения()
        
        # Настраиваем стиль через ttk.Style
        style = ttk.Style()
        style.configure('Custom.TLabelframe', relief='solid')
        style.configure('Menu.TLabelframe', relief='solid')
        style.configure("Treeview", background='#f0f0f0')
        
        # Фрейм_основной_контейнер с новым стилем
        self.фрейм_основной_контейнер = ttk.LabelFrame(self, width=1000, borderwidth=1, 
                                                       text="_основной_контейнер_", style='Custom.TLabelframe')
        self.фрейм_основной_контейнер.pack(expand=True, fill= 'y')

        # Фрейм_меню с новым стилем
        фрейм_меню = ttk.LabelFrame(self.фрейм_основной_контейнер, width=200, borderwidth=1, 
                                   text="_меню_", style='Custom.TLabelframe')
        фрейм_меню.pack(expand=True, fill= 'y', side= 'left')

        # Фрейм_данные с новым стилем
        фрейм_данные = ttk.LabelFrame(self.фрейм_основной_контейнер, width=800, borderwidth=1, 
                                     text="_контент_", style='Custom.TLabelframe')
        фрейм_данные.pack(expand=True, fill= 'y', side= 'left')

        # Создаем notebook во фрейме данных
        self.фрейм_с_вкладками_контент = ttk.Notebook(фрейм_данные, width=800)
        self.фрейм_с_вкладками_контент.pack(expand=True, fill='both')
        
        # Словарь для хранения вкладок и кнопок
        self.вкладки = {}
        self.кнопки = {}

        # Добавляем словарь для хранения состояний вкладок и индикаторов
        self.состояния_вкладок = {}
        self.индикаторы = {}

        # Загружаем иконки для разных состояний
        пустая_иконка = Image.new('RGBA', (16, 16), (0, 0, 0, 0))  # Создаем прозрачную иконку
        self.иконки = {
            "не_начато": ImageTk.PhotoImage(пустая_иконка),
            "в_процессе": ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(__file__), 'assets', 'file-edit.png')).resize((16, 16))),
            "завершено": ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(__file__), 'assets', 'file-check.png')).resize((16, 16)))
        }
        
        # Создаем группу Приказы
        группа_приказы = ttk.LabelFrame(фрейм_меню, text="Приказы", 
                                       padding=5, style='Menu.TLabelframe')
        группа_приказы.pack(fill='x', padx=5, pady=5)
        
        # Словарь для хранения приказов и их состояний
        self.приказы = ["Суточный приказ", "Приказ изменений"]
        
        # Создаем кнопки меню с индикаторами
        for название_кнопки, текст_кнопки in [
            ("Суточный приказ", "Новый суточный приказ"),
            ("Приказ изменений", "Приказ внесения изменений")
        ]:
            контейнер = tk.Frame(группа_приказы)
            контейнер.pack(fill='x', pady=2)
            
            # Создаем индикатор состояния
            self.индикаторы[название_кнопки] = tk.Label(
                контейнер,
                image=self.иконки["не_начато"],  # Устанавливаем пустую иконку
                bg='#f0f0f0',
                width=16,
                height=2
            )
            self.индикаторы[название_кнопки].pack(side='left', fill='y')  # Добавляем fill='y' для вертикального заполнения
            
            self.кнопки[название_кнопки] = tk.Button(
                контейнер,
                text=текст_кнопки,
                command=lambda н=название_кнопки: self.открыть_вкладку(н),
                **self.стили.button_config
            )
            self.кнопки[название_кнопки].pack(side='left', fill='x', expand=True)
            self.состояния_вкладок[название_кнопки] = "не_начато"

        # Создаем группу Списки сотрудников
        группа_списки = ttk.LabelFrame(фрейм_меню, text="Списки сотрудников", 
                                      padding=5, style='Menu.TLabelframe')
        группа_списки.pack(fill='x', padx=5)

        # Создаем кнопки и привязываем к ним обработчики
        self.кнопки["Список офицеров"] = tk.Button(
            группа_списки, 
            text="Список офицеров",
            command=lambda: self.открыть_вкладку("Список офицеров"),
            **self.стили.button_config
        )
        self.кнопки["Список офицеров"].pack(pady=2, fill='x')
        
        self.кнопки["Список курсантов"] = tk.Button(
            группа_списки, 
            text="Список курсантов",
            command=lambda: self.открыть_вкладку("Список курсантов"),
            **self.стили.button_config
        )
        self.кнопки["Список курсантов"].pack(pady=2, fill='x')

    def открыть_вкладку(self, название):
        # Сброс цвета всех кнопок и индикаторов
        for имя_кнопки in self.кнопки:
            self.кнопки[имя_кнопки].configure(bg='#f0f0f0')
            if имя_кнопки in self.приказы:
                self.индикаторы[имя_кнопки].configure(bg='#f0f0f0')
        
        # Установка цвета активной кнопки и индикатора
        self.кнопки[название].configure(bg='lightblue')
        if название in self.приказы:
            self.индикаторы[название].configure(bg='lightblue')
        
        # Проверяем, существует ли уже такая вкладка
        if название not in self.вкладки:
            if название == "Суточный приказ":
                новая_вкладка = ttk.Frame(self.фрейм_с_вкладками_контент)
                self.фрейм_с_вкладками_контент.add(новая_вкладка, text=название)
                self.вкладки[название] = новая_вкладка
                # Вставляем кастомный фрейм приказа
                приказ_виджет = ПриказСлужебныйНаряд(новая_вкладка)
                приказ_виджет.pack(fill=tk.BOTH, expand=True)
            else:
                новая_вкладка = ttk.Frame(self.фрейм_с_вкладками_контент)
                self.фрейм_с_вкладками_контент.add(новая_вкладка, text=название)
                self.вкладки[название] = новая_вкладка
            if название in self.приказы:
                self.состояния_вкладок[название] = "в_процессе"
                self.индикаторы[название].configure(image=self.иконки["в_процессе"])
        
        # Переключаемся на вкладку
        индекс_вкладки = self.фрейм_с_вкладками_контент.index(self.вкладки[название])
        self.фрейм_с_вкладками_контент.select(индекс_вкладки)
        

if __name__ == "__main__":
    # Создание главного окна
    главное_окно = ГлавноеОкно()
    # Запуск главного цикла приложения
    главное_окно.mainloop()