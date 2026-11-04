# history.py
from datetime import datetime
from typing import List, Dict, Optional

class History:
    """
    Класс для управления историей действий.
    Хранит записи с отметками времени.
    """
    
    def __init__(self, max_size: int = 100):
        """
        Инициализация истории.
        
        Args:
            max_size (int): Максимальное количество записей
        """
        self._entries: List[Dict[str, str]] = []
        self._max_size = max_size
    
    def add(self, action: str) -> None:
        """
        Добавляет запись в историю.
        
        Args:
            action (str): Описание действия
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._entries.append({
            "timestamp": timestamp,
            "action": action
        })
        
        # Обрезаем историю, если превышен лимит
        if len(self._entries) > self._max_size:
            self._entries = self._entries[-self._max_size:]
    
    def get_all(self) -> List[Dict[str, str]]:
        """
        Возвращает все записи истории.
        
        Returns:
            List[Dict[str, str]]: Список записей
        """
        return self._entries.copy()
    
    def get_last(self, count: int = 10) -> List[Dict[str, str]]:
        """
        Возвращает последние N записей.
        
        Args:
            count (int): Количество записей
        
        Returns:
            List[Dict[str, str]]: Список последних записей
        """
        return self._entries[-count:].copy()
    
    def clear(self) -> None:
        """Очищает всю историю."""
        self._entries.clear()
    
    def get_size(self) -> int:
        """
        Возвращает количество записей.
        
        Returns:
            int: Количество записей
        """
        return len(self._entries)
    
    def export_to_text(self) -> str:
        """
        Экспортирует историю в текстовый формат.
        
        Returns:
            str: История в виде текста
        """
        if not self._entries:
            return "История пуста"
        
        lines = ["=== ИСТОРИЯ ДЕЙСТВИЙ ===\n"]
        for entry in self._entries:
            lines.append(f"[{entry['timestamp']}] {entry['action']}")
        
        return "\n".join(lines)
    
    def find(self, keyword: str) -> List[Dict[str, str]]:
        """
        Ищет записи по ключевому слову.
        
        Args:
            keyword (str): Ключевое слово для поиска
        
        Returns:
            List[Dict[str, str]]: Найденные записи
        """
        keyword_lower = keyword.lower()
        return [
            entry for entry in self._entries 
            if keyword_lower in entry["action"].lower()
        ]