import json
import os
from pathlib import Path

class СогласованиеСохранение:
    """
    Класс для хранения и управления информацией о согласующих лицах приказов.
    Сохраняет данные в JSON-файл для постоянного хранения.
    """
    def __init__(self):
        self.data = {}
        # Файл настроек согласующих хранится в корне проекта под именем data_approvers.json
        # Определяем корень проекта как parent папки, где расположен модуль (один уровень выше папки Служебный_наряд)
        project_root = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))).resolve()
        self.storage_path = project_root / "data_approvers.json"
        self._load()

    def _load(self):
        """Загружает данные из JSON-файла, если он существует."""
        default_path = self.storage_path.parent / 'default_approvers.json'
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.data = {}
            # Если файл существует, но пустой — попытаемся инициализировать из default
            if not self.data and default_path.exists():
                try:
                    with open(default_path, 'r', encoding='utf-8') as f:
                        self.data = json.load(f)
                    self._save()
                except (json.JSONDecodeError, IOError):
                    self.data = {}
        else:
            # Попробовать инициализировать из default_approvers.json в корне проекта
            if default_path.exists():
                try:
                    with open(default_path, 'r', encoding='utf-8') as f:
                        self.data = json.load(f)
                    # Сохранить в data_approvers.json для дальнейшего использования
                    self._save()
                except (json.JSONDecodeError, IOError):
                    self.data = {}
            else:
                self.data = {}

    def _save(self):
        """Сохраняет данные в JSON-файл."""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except IOError:
            pass  # Обработка ошибки записи

    def get(self, order_type, role):
        """
        Получает список ID офицеров для указанного типа приказа и роли.
        
        Args:
            order_type (str): Тип приказа (например, 'суточный приказ')
            role (str): Роль офицера ('руководитель', 'контроль', 'согласование')
            
        Returns:
            list: Список ID офицеров
        """
        if order_type not in self.data:
            return []
        if role not in self.data[order_type]:
            return []
        return self.data[order_type][role]

    def set(self, order_type, role, officer_ids):
        """
        Устанавливает список ID офицеров для указанного типа приказа и роли.
        
        Args:
            order_type (str): Тип приказа (например, 'суточный приказ')
            role (str): Роль офицера ('руководитель', 'контроль', 'согласование')
            officer_ids (list): Список ID офицеров
        """
        if order_type not in self.data:
            self.data[order_type] = {}
        self.data[order_type][role] = officer_ids
        self._save()

    def clear(self, order_type=None, role=None):
        """
        Очищает данные для указанного типа приказа и/или роли.
        Если параметры не указаны, очищает все данные.
        
        Args:
            order_type (str, optional): Тип приказа
            role (str, optional): Роль офицера
        """
        if order_type is None:
            self.data = {}
        elif role is None and order_type in self.data:
            self.data[order_type] = {}
        elif order_type in self.data and role in self.data[order_type]:
            self.data[order_type][role] = []
        self._save()