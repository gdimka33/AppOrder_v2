from tkinter import ttk

class СтилиПриложения:
    def __init__(self):
        self.style = ttk.Style()
        
        # Настраиваем стиль для основных LabelFrame
        self.style.configure('Custom.TLabelframe.Label', 
                           font=('Arial', 10, 'bold'))
        self.style.configure('Custom.TLabelframe', 
                           labelmargins=2)
        
        # Настраиваем стиль для групп меню
        self.style.configure('Menu.TLabelframe.Label', 
                           font=('Arial', 9),
                           foreground='gray')
        self.style.configure('Menu.TLabelframe', 
                           labelmargins=2)
        
        # Параметры для кнопок меню
        self.button_config = {
            'relief': 'flat',
            'bg': '#f0f0f0',
            'activebackground': '#e5e5e5',
            'borderwidth': 1,
            'padx': 10
        }
