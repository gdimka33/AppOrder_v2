import tkinter as tk
from tkinter import ttk

class ОфицерИнфо(tk.Label):
    def __init__(self, master=None, officer_id=None, **kwargs):
        # Ensure we have valid kwargs for tk.Label
        label_kwargs = kwargs.copy()
        
        # Set default values if not provided
        if 'text' not in label_kwargs:
            label_kwargs['text'] = 'Загрузка...'
        if 'cursor' not in label_kwargs:
            label_kwargs['cursor'] = 'hand2'
            
        # Initialize the tk.Label
        super().__init__(master, **label_kwargs)
        
        # Store officer_id and bind events
        self.officer_id = officer_id
        self.bind('<Enter>', self._show_tooltip)
        self.bind('<Leave>', self._hide_tooltip)
        
        # Создаем стиль для всплывающего окна
        style = ttk.Style()
        # Просто настраиваем стили для всплывающего окна
        style.configure('Tooltip.TFrame', background='#f5f5f5')
        style.configure('Tooltip.TLabel', background='#f5f5f5')

    def _load_officer_data(self):
        # Проверяем, есть ли officer_id
        if not self.officer_id:
            return {
                'звание': '',
                'фио': 'Не выбран',
                'полное_фио': 'Офицер не выбран',
                'подразделение': '',
                'должность': ''
            }
        
        # Если у нас есть сохраненные данные офицера, используем их
        if hasattr(self, 'officer_data') and self.officer_data:
            return self.officer_data
            
        # Здесь будет логика загрузки данных по officer_id
        # В реальном приложении здесь должен быть запрос к базе данных или справочнику
        return {
            'звание': 'Капитан',
            'фио': 'Иванов И.И.',
            'полное_фио': 'Иванов Иванович',
            'подразделение': 'Отдел кадров',
            'должность': 'Начальник отдела'
        }

    def _show_tooltip(self, event=None):
        # Only show tooltip if we have officer data
        if not self.officer_id and self.cget('text') in ['Выбрать', 'Загрузка...']:
            return
            
        data = self._load_officer_data()
        self.tooltip = tk.Toplevel(self)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f'+{event.x_root+15}+{event.y_root+10}')
        
        # Устанавливаем светлый фон для всплывающего окна
        self.tooltip.configure(bg='#f0f0f0')
        
        info_frame = ttk.Frame(self.tooltip, padding=5, style='Tooltip.TFrame')
        info_frame.pack()
        
        # Display officer information
        if data['звание']:
            ttk.Label(info_frame, text=f"Звание: {data['звание']}", style='Tooltip.TLabel').pack(anchor='w')
        ttk.Label(info_frame, text=f"ФИО: {data['полное_фио']}", style='Tooltip.TLabel').pack(anchor='w')
        if data['подразделение']:
            ttk.Label(info_frame, text=f"Подразделение: {data['подразделение']}", style='Tooltip.TLabel').pack(anchor='w')
        if data['должность']:
            ttk.Label(info_frame, text=f"Должность: {data['должность']}", style='Tooltip.TLabel').pack(anchor='w')

    def _hide_tooltip(self, event=None):
        if hasattr(self, 'tooltip') and self.tooltip.winfo_exists():
            self.tooltip.destroy()

    def update_info(self, officer_id=None, officer_data=None):
        if officer_id:
            self.officer_id = officer_id
            
        # Сохраняем данные офицера, если они переданы
        if officer_data:
            self.officer_data = officer_data
            
        # Only update text if we have an officer_id
        if self.officer_id:
            data = self._load_officer_data()
            # Проверяем, есть ли звание, и форматируем текст соответственно
            if data['звание']:
                self.configure(
                    text=f"{data['звание']} {data['фио']}",
                    font=("TkDefaultFont", 9, "normal")
                )
            else:
                self.configure(
                    text=f"{data['фио']}",
                    font=("TkDefaultFont", 9, "normal")
                )
        return self