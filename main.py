from library import Library
from utils import *
import sys


class LibraryApp:
    """Консольное приложение библиотеки"""

    def __init__(self):
        self.library = Library()
        self.commands = {
            '1': self.add_book,
            '2': self.view_books,
            '3': self.view_favorites,
            '4': self.search_books,
            '5': self.manage_book,
            '6': self.recommendations,
            '0': self.exit_app
        }

    def run(self):
        """Запуск приложения"""
        while True:
            self.show_menu()
            choice = input("\nВыберите действие: ").strip()

            if choice in self.commands:
                self.commands[choice]()
            else:
                print("Неверный выбор. Пожалуйста, попробуйте снова.")

    def show_menu(self):
        """Отображение главного меню"""
        clear_screen()
        print_header("T-БИБЛИОТЕКА")
        print("1. Добавить книгу")
        print("2. Просмотр книг")
        print("3. Избранное")
        print("4. Поиск книг")
        print("5. Управление книгой")
        print("6. Рекомендации")
        print("0. Выход")

    def add_book(self):
        """Добавление новой книги"""
        clear_screen()
        print_header("ДОБАВЛЕНИЕ КНИГИ")

        title = input_with_validation("Название: ")
        author = input_with_validation("Автор: ")
        genre = input_with_validation("Жанр: ")

        def validate_year(y):
            try:
                year = int(y)
                return 1000 <= year <= 2025
            except ValueError:
                return False

        year = int(input_with_validation(
            "Год издания: ",
            validate_year,
            "Введите корректный год (1000-2025)"
        ))

        description = input("Краткое описание: ")

        book = self.library.add_book(title, author, genre, year, description)
        print(f"\nКнига '{book.title}' успешно добавлена с ID: {book.id}")
        input("\nНажмите Enter для продолжения...")

    def view_books(self):
        """Просмотр книг с сортировкой и фильтрацией"""
        clear_screen()
        print_header("ПРОСМОТР КНИГ")

        print("Сортировка:")
        print("1. По названию")
        print("2. По автору")
        print("3. По году")
        print("4. По жанру")
        print("5. Без сортировки")

        sort_choice = input("\nВыберите сортировку (1-5): ").strip()

        sort_map = {
            '1': 'title',
            '2': 'author',
            '3': 'year',
            '4': 'genre'
        }

        books = self.library.get_all_books()

        if sort_choice in sort_map:
            reverse = input("По убыванию? (д/н): ").lower() == 'д'
            books = self.library.sort_books(sort_map[sort_choice], reverse)

        print("\nФильтрация:")
        filter_by = input("Фильтровать по жанру? (ж) / статусу? (с) / пропустить (enter): ").lower()

        if filter_by == 'ж':
            genre = input("Введите жанр: ")
            books = self.library.filter_books(genre=genre)
        elif filter_by == 'с':
            status = input("Статус (прочитана/не прочитана): ")
            books = self.library.filter_books(status=status)

        clear_screen()
        print_books(books)
        input("\nНажмите Enter для продолжения...")

    def view_favorites(self):
        """Просмотр избранных книг"""
        clear_screen()
        favorites = self.library.get_favorites()
        print_books(favorites, "ИЗБРАННЫЕ КНИГИ")
        input("\nНажмите Enter для продолжения...")

    def search_books(self):
        """Поиск книг"""
        clear_screen()
        print_header("ПОИСК КНИГ")

        query = input("Введите поисковый запрос: ")
        results = self.library.search_books(query)

        print_books(results, f"РЕЗУЛЬТАТЫ ПОИСКА: '{query}'")
        input("\nНажмите Enter для продолжения...")

    def manage_book(self):
        """Управление конкретной книгой"""
        clear_screen()
        print_header("УПРАВЛЕНИЕ КНИГОЙ")

        try:
            book_id = int(input("Введите ID книги: "))

            # Находим книгу
            book = None
            for b in self.library.books:
                if b.id == book_id:
                    book = b
                    break

            if not book:
                print("Книга не найдена")
                input("\nНажмите Enter для продолжения...")
                return

            print(f"\nТекущая книга: {book}")
            print("\nДействия:")
            print("1. Изменить статус")
            print("2. Добавить/удалить из избранного")
            print("3. Удалить книгу")
            print("0. Назад")

            choice = input("\nВыберите действие: ").strip()

            if choice == '1':
                status = input("Новый статус (прочитана/не прочитана): ")
                if self.library.change_status(book_id, status):
                    print("Статус обновлен")
                else:
                    print("Ошибка обновления статуса")

            elif choice == '2':
                is_favorite = book_id in self.library.favorites
                action = "удалена из" if is_favorite else "добавлена в"
                self.library.toggle_favorite(book_id)
                print(f"Книга {action} избранное")

            elif choice == '3':
                confirm = input(f"Удалить книгу '{book.title}'? (д/н): ")
                if confirm.lower() == 'д':
                    if self.library.delete_book(book_id):
                        print("Книга удалена")
                    else:
                        print("Ошибка удаления")

        except ValueError:
            print("Неверный ID")

        input("\nНажмите Enter для продолжения...")

    def recommendations(self):
        """Просмотр рекомендаций"""
        clear_screen()
        print_header("РЕКОМЕНДАЦИИ ДЛЯ ВАС")

        recommendations = self.library.get_recommendations()

        if recommendations:
            print_books(recommendations)
        else:
            print("Нет рекомендаций. Добавьте книги в избранное!")

        input("\nНажмите Enter для продолжения...")

    def exit_app(self):
        """Выход из приложения"""
        print("\nСпасибо за использование T-Библиотеки!")
        sys.exit(0)


if __name__ == "__main__":
    app = LibraryApp()
    app.run()