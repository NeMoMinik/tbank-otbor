import pytest
import os
from library import Library
from models import Book


@pytest.fixture
def library():
    """Фикстура для создания чистой библиотеки перед каждым тестом"""
    lib = Library()
    # Очищаем данные
    lib.books = []
    lib.favorites = []
    lib._next_id = 1
    return lib


def test_add_book(library):
    """Тест добавления книги"""
    book = library.add_book("Тест", "Автор", "Жанр", 2023, "Описание")
    assert len(library.books) == 1
    assert book.id == 1
    assert book.title == "Тест"


def test_sort_books(library):
    """Тест сортировки книг"""
    library.add_book("Б", "Автор2", "Жанр", 2020, "Описание")
    library.add_book("А", "Автор1", "Жанр", 2023, "Описание")

    sorted_books = library.sort_books('title')
    assert sorted_books[0].title == "А"
    assert sorted_books[1].title == "Б"


def test_filter_books(library):
    """Тест фильтрации книг"""
    library.add_book("Книга1", "Автор1", "Фантастика", 2020, "Описание")
    library.add_book("Книга2", "Автор2", "Роман", 2023, "Описание")

    filtered = library.filter_books(genre="Фантастика")
    assert len(filtered) == 1
    assert filtered[0].title == "Книга1"


def test_favorites(library):
    """Тест работы с избранным"""
    book = library.add_book("Тест", "Автор", "Жанр", 2023, "Описание")

    # Добавляем в избранное
    result = library.toggle_favorite(book.id)
    assert result == True
    assert book.id in library.favorites

    # Удаляем из избранного
    result = library.toggle_favorite(book.id)
    assert result == False
    assert book.id not in library.favorites


def test_change_status(library):
    """Тест изменения статуса"""
    book = library.add_book("Тест", "Автор", "Жанр", 2023, "Описание")

    result = library.change_status(book.id, "прочитана")
    assert result == True
    assert book.status == "прочитана"


def test_delete_book(library):
    """Тест удаления книги"""
    book = library.add_book("Тест", "Автор", "Жанр", 2023, "Описание")
    assert len(library.books) == 1

    result = library.delete_book(book.id)
    assert result == True
    assert len(library.books) == 0


def test_search_books(library):
    """Тест поиска книг"""
    library.add_book("Война и мир", "Толстой", "Роман", 1869, "О войне")
    library.add_book("Преступление", "Достоевский", "Роман", 1866, "О наказании")

    results = library.search_books("война")
    assert len(results) == 1
    assert results[0].title == "Война и мир"


def test_recommendations(library):
    """Тест рекомендаций"""
    # Добавляем книги
    book1 = library.add_book("Книга1", "Автор1", "Фантастика", 2020, "Описание")
    book2 = library.add_book("Книга2", "Автор1", "Фантастика", 2021, "Описание")
    book3 = library.add_book("Книга3", "Автор2", "Роман", 2022, "Описание")

    # Добавляем в избранное книги одного автора и жанра
    library.toggle_favorite(book1.id)

    recommendations = library.get_recommendations()
    assert len(recommendations) > 0
    assert recommendations[0].id == book2.id  # Должна рекомендовать похожую книгу