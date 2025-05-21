import tkinter as tk
from tkinter import ttk
from logger import logger
from стили import СтилиПриложения

logger.info('Приложение запущено')

class ГлавноеОкно(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Учёт личного состава")
        self.state('zoomed')

        # Инициализируем стили
        self.стили = СтилиПриложения()
        
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

        # Базовые параметры кнопок
        button_config = {
            'relief': 'flat',
            'bg': '#f0f0f0',
            'activebackground': '#e5e5e5',
            'borderwidth': 1,
            'padx': 10
        }
        
        # Создаем группу Приказы
        группа_приказы = ttk.LabelFrame(фрейм_меню, text="Приказы", 
                                       padding=5, style='Menu.TLabelframe')
        группа_приказы.pack(fill='x', padx=5, pady=5)
        
        # Создаем кнопки меню
        self.кнопки["Суточный приказ"] = tk.Button(
            группа_приказы, 
            text="Новый суточный приказ",
            command=lambda: self.открыть_вкладку("Суточный приказ"),
            **self.стили.button_config
        )
        self.кнопки["Суточный приказ"].pack(pady=2, fill='x')
        
        # Аналогично меняем остальные кнопки
        self.кнопки["Приказ изменений"] = tk.Button(
            группа_приказы, 
            text="Приказ внесения изменений",
            command=lambda: self.открыть_вкладку("Приказ изменений"),
            **self.стили.button_config
        )
        self.кнопки["Приказ изменений"].pack(pady=2, fill='x')

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
        # Сброс цвета всех кнопок
        for кнопка in self.кнопки.values():
            кнопка.configure(bg='#f0f0f0')
        
        # Установка цвета активной кнопки
        self.кнопки[название].configure(bg='lightblue')
        
        # Проверяем, существует ли уже такая вкладка
        if название not in self.вкладки:
            новая_вкладка = ttk.Frame(self.фрейм_с_вкладками_контент)
            self.фрейм_с_вкладками_контент.add(новая_вкладка, text=название)
            self.вкладки[название] = новая_вкладка
            
        # Переключаемся на вкладку
        индекс_вкладки = self.фрейм_с_вкладками_контент.index(self.вкладки[название])
        self.фрейм_с_вкладками_контент.select(индекс_вкладки)
        

if __name__ == "__main__":
    # Создание главного окна
    главное_окно = ГлавноеОкно()
    # Запуск главного цикла приложения
    главное_окно.mainloop()