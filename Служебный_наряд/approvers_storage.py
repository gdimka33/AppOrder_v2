import os
import json
import sys

class ApproversStorage:
    def __init__(self, filename=None):
        self.filename = filename or self._get_default_file()
        self.data = self._load()

    @staticmethod
    def _get_default_file():
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__import__('__main__').__file__))
        return os.path.join(base_dir, 'default_approvers.json')

    def _load(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump({}, f)
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Миграция старого формата (list вместо dict по ролям)
            changed = False
            for order_type, value in list(data.items()):
                if isinstance(value, list):
                    # Старый формат: просто список id для согласования
                    data[order_type] = {'согласование': value}
                    changed = True
            if changed:
                with open(self.filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            return data
        except Exception:
            return {}

    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def get(self, order_type, role):
        return self.data.get(order_type, {}).get(role, [])

    def set(self, order_type, role, officers):
        if order_type not in self.data:
            self.data[order_type] = {}
        self.data[order_type][role] = officers
        self.save()

    def get_all_roles(self, order_type):
        return self.data.get(order_type, {})
