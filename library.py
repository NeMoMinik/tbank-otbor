from typing import List, Optional, Callable
from models import Book
from storage import Storage


class Library:
    """Основной класс библиотеки"""

    def __init__(self):
        self.storage = Storage()
        self.books = self.storage.load_books()
        self.favorites = self.storage.load_favorites()
        self._next_id = self._get_max_id() + 1 if self.books else 1

    def _get_max_id(self) -> int:
        """Получение максимального ID среди книг"""
        if not self.books:
            return 0
        return max(book.id for book in self.books)

    def _assign_ids(self):
        """Присвоение ID книгам при загрузке"""
        for i, book in enumerate(self.books, 1):
            book.id = i
        self._next_id = len(self.books) + 1

    def add_book(self, title: str, author: str, genre: str,
                 year: int, description: str) -> Book:
        """Добавление новой книги"""
        book = Book(
            id=self._next_id,
            title=title,
            author=author,
            genre=genre,
            year=year,
            description=description
        )
        self.books.append(book)
        self._next_id += 1
        self.storage.save_books(self.books)
        return book

    def get_all_books(self) -> List[Book]:
        """Получение всех книг"""
        return self.books

    def sort_books(self, key: str, reverse: bool = False) -> List[Book]:
        """Сортировка книг"""
        valid_keys = {
            'title': lambda b: b.title.lower(),
            'author': lambda b: b.author.lower(),
            'year': lambda b: b.year,
            'genre': lambda b: b.genre.lower()
        }

        if key not in valid_keys:
            raise ValueError(f"Недопустимый ключ сортировки. Используйте: {list(valid_keys.keys())}")

        return sorted(self.books, key=valid_keys[key], reverse=reverse)

    def filter_books(self, genre: Optional[str] = None,
                     status: Optional[str] = None) -> List[Book]:
        """Фильтрация книг"""
        result = self.books.copy()

        if genre:
            result = [b for b in result if b.genre.lower() == genre.lower()]

        if status:
            result = [b for b in result if b.status.lower() == status.lower()]

        return result

    def toggle_favorite(self, book_id: int) -> bool:
        """Добавление/удаление книги из избранного"""
        if book_id in self.favorites:
            self.favorites.remove(book_id)
            self.storage.save_favorites(self.favorites)
            return False
        else:
            self.favorites.append(book_id)
            self.storage.save_favorites(self.favorites)
            return True

    def get_favorites(self) -> List[Book]:
        """Получение списка избранных книг"""
        return [book for book in self.books if book.id in self.favorites]

    def change_status(self, book_id: int, status: str) -> bool:
        """Изменение статуса книги"""
        if status not in ['прочитана', 'не прочитана']:
            raise ValueError("Статус должен быть 'прочитана' или 'не прочитана'")

        for book in self.books:
            if book.id == book_id:
                book.status = status
                self.storage.save_books(self.books)
                return True
        return False

    def delete_book(self, book_id: int) -> bool:
        """Удаление книги из библиотеки"""
        for i, book in enumerate(self.books):
            if book.id == book_id:
                del self.books[i]
                # Удаляем из избранного, если была там
                if book_id in self.favorites:
                    self.favorites.remove(book_id)
                    self.storage.save_favorites(self.favorites)
                self.storage.save_books(self.books)
                return True
        return False

    def search_books(self, query: str) -> List[Book]:
        """Поиск книг по ключевым словам"""
        query = query.lower()
        result = []

        for book in self.books:
            if (query in book.title.lower() or
                    query in book.author.lower() or
                    query in book.description.lower()):
                result.append(book)

        return result

    def get_recommendations(self) -> List[Book]:
        """Получение рекомендаций на основе избранного"""
        if not self.favorites:
            return []

        # Анализируем жанры из избранного
        favorite_books = self.get_favorites()
        genres = {}
        authors = {}

        for book in favorite_books:
            genres[book.genre] = genres.get(book.genre, 0) + 1
            authors[book.author] = authors.get(book.author, 0) + 1

        # Находим популярные жанры и авторов
        top_genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)[:2]
        top_authors = sorted(authors.items(), key=lambda x: x[1], reverse=True)[:2]

        # Рекомендуем книги, которых нет в избранном
        recommendations = []
        for book in self.books:
            if book.id in self.favorites:
                continue

            score = 0
            for genre, _ in top_genres:
                if book.genre == genre:
                    score += 1

            for author, _ in top_authors:
                if book.author == author:
                    score += 2  # Автор важнее жанра

            if score > 0:
                recommendations.append((score, book))

        # Сортируем по релевантности
        recommendations.sort(reverse=True)
        return [book for score, book in recommendations[:5]]