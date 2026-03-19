def clear_screen():
    """Очистка экрана"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(text):
    """Печать заголовка"""
    print("=" * 60)
    print(f"{text:^60}")
    print("=" * 60)


def print_book(book, index=None):
    """Печать информации о книге"""
    prefix = f"{index}. " if index else ""
    print(f"{prefix}[ID: {book.id}] {book.title}")
    print(f"   Автор: {book.author}")
    print(f"   Жанр: {book.genre}")
    print(f"   Год: {book.year}")
    print(f"   Статус: {book.status}")
    print(f"   Описание: {book.description[:100]}..." if len(
        book.description) > 100 else f"   Описание: {book.description}")
    print()


def print_books(books, title="Список книг"):
    """Печать списка книг"""
    print_header(title)
    if not books:
        print("Библиотека пуста")
    else:
        for i, book in enumerate(books, 1):
            print_book(book, i)
    print()


def input_with_validation(prompt, validator=None, error_msg="Неверный ввод"):
    """Ввод с валидацией"""
    while True:
        value = input(prompt).strip()
        if not value:
            print("Значение не может быть пустым")
            continue

        if validator:
            try:
                if validator(value):
                    return value
                else:
                    print(error_msg)
            except ValueError:
                print(error_msg)
        else:
            return value