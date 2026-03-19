import pytest
import json
import os
from storage import Storage
from models import Book


@pytest.fixture
def storage():
    """Фикстура для создания временного хранилища"""
    return Storage()


def test_save_and_load_books(tmp_path, storage):
    """Тест сохранения и загрузки книг"""
    # Меняем пути на временные
    storage.books_file = tmp_path / "test_books.json"

    books = [
        Book("Книга1", "Автор1", "Жанр1", 2020, "Описание1", id=1),
        Book("Книга2", "Автор2", "Жанр2", 2021, "Описание2", id=2)
    ]

    # Сохраняем
    storage.save_books(books)
    assert os.path.exists(storage.books_file)

    # Загружаем
    loaded_books = storage.load_books()
    assert len(loaded_books) == 2
    assert loaded_books[0].title == "Книга1"
    assert loaded_books[1].author == "Автор2"


def test_save_and_load_favorites(tmp_path, storage):
    """Тест сохранения и загрузки избранного"""
    storage.favorites_file = tmp_path / "test_favorites.json"

    favorites = [1, 3, 5]

    # Сохраняем
    storage.save_favorites(favorites)
    assert os.path.exists(storage.favorites_file)

    # Загружаем
    loaded_favorites = storage.load_favorites()
    assert loaded_favorites == [1, 3, 5]


