import json
import os
from typing import List, Dict, Any
from config import Config
from models import Book


class Storage:
    """Класс для работы с файловым хранилищем"""

    def __init__(self):
        self.books_file = Config.BOOKS_DB
        self.favorites_file = Config.FAVORITES_DB

    def save_books(self, books: List[Book]):
        """Сохранение списка книг в файл"""
        data = [book.to_dict() for book in books]
        with open(self.books_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_books(self) -> List[Book]:
        """Загрузка списка книг из файла"""
        if not os.path.exists(self.books_file):
            return []

        with open(self.books_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return [Book.from_dict(book_data) for book_data in data]

    def save_favorites(self, favorites: List[int]):
        """Сохранение списка избранных книг"""
        with open(self.favorites_file, 'w', encoding='utf-8') as f:
            json.dump(favorites, f, ensure_ascii=False, indent=4)

    def load_favorites(self) -> List[int]:
        """Загрузка списка избранных книг"""
        if not os.path.exists(self.favorites_file):
            return []

        with open(self.favorites_file, 'r', encoding='utf-8') as f:
            return json.load(f)