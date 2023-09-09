import os


class NoteManager:
    def __init__(self, note_folder):
        self.note_folder = note_folder

    def create_note(self, title, content, tags):
        note_path = os.path.join(self.note_folder, f"{title}.txt")
        with open(note_path, "w") as file:
            file.write(f"Заголовок: {title}\n")
            file.write(f"Зміст: {content}\n")
            file.write(f"Теги: {', '.join(tags)}\n")

    def search_notes_by_tags(self, tags):
        matching_notes = []
        for filename in os.listdir(self.note_folder):
            if filename.endswith(".txt"):
                with open(os.path.join(self.note_folder, filename), "r") as file:
                    content = file.read()
                    if all(tag in content for tag in tags):
                        matching_notes.append(content)

        if matching_notes:
            print(f"Нотатки, що містять теги {tags}")
            for note in matching_notes:
                print("-" * 20)
                print(note)
        else:
            print(f"Нотатки з тегами {tags} не знайдено")

    def search_notes_by_title(self, title):
        matching_notes = []
        for filename in os.listdir(self.note_folder):
            if filename.endswith(".txt") and title in filename:
                note_path = os.path.join(self.note_folder, filename)
                with open(note_path, "r") as file:
                    note_content = file.read()
                    matching_notes.append(note_content)

        if matching_notes:
            print(f"Нотатки, за назвою {title}")
            for note in matching_notes:
                print("-" * 20)
                print(note)
        else:
            print(f"Нотатки з назвою {title} не знайдено")

    def display_all_notes(self):
        for filename in os.listdir(self.note_folder):
            if filename.endswith(".txt"):
                note_path = os.path.join(self.note_folder, filename)
                with open(note_path, "r") as file:
                    note_content = file.read()
                    print(note_content)
                    print("-" * 20)  # Розділювач між нотатками

    def edit_note(self, title, new_content):
        note_path = os.path.join(self.note_folder, f"{title}.txt")
        if os.path.exists(note_path):
            with open(note_path, "w") as file:
                file.write(f"Заголовок: {title}\n")
                file.write(f"Зміст: {new_content}\n")

    def delete_note(self, title):
        note_path = os.path.join(self.note_folder, f"{title}.txt")
        if os.path.exists(note_path):
            os.remove(note_path)

    def nb_main(self):
        # Переконайтеся, що папка для зберігання нотаток існує
        if not os.path.exists(self.note_folder):
            os.makedirs(self.note_folder)

        while True:
            print("\nМеню:")
            print("1. Створити нотатку")
            print("2. Пошук нотаток за тегами")
            print("3. Пошук нотаток за назвою")
            print("4. Відобразити всі нотатки")
            print("5. Редагувати нотатку")
            print("6. Видалити нотатку")
            print("7. Вийти")

            choice = input("Виберіть опцію: ")

            if choice == "1":
                title = input("Введіть назву нотатки: ")
                content = input("Введіть зміст нотатки: ")
                tags = input("Введіть теги (через кому): ").split(", ")
                self.create_note(title, content, tags)
                print("Нотатка створена.")

            elif choice == "2":
                tags_to_search = input("Введіть теги для пошуку (через кому): ").split(", ")
                self.search_notes_by_tags(tags_to_search)

            elif choice == "3":
                title_to_search = input("Введіть назву для пошуку: ")
                self.search_notes_by_title(title_to_search)

            elif choice == "4":
                print("\n" + ("-" * 20))
                self.display_all_notes()

            elif choice == "5":
                title = input("Введіть назву нотатки для редагування: ")
                new_content = input("Введіть новий зміст нотатки: ")
                self.edit_note(title, new_content)
                print("Нотатка оновлена.")

            elif choice == "6":
                title = input("Введіть назву нотатки для видалення: ")
                self.delete_note(title)
                print("Нотатка видалена.")

            elif choice == "7":
                break

            else:
                print("Невірний вибір. Будь ласка, виберіть коректну опцію.")


if __name__ == "__main__":
    """
    В меню використовуй код, який я напишу тут у коментарях
    ------------------------------
    from notebook.nb_main import NoteManager
    note_folder = "notebook/notes"
    manager = NoteManager(note_folder)
    manager.nb_main()
    ------------------------------
    """

    note_folder = "notes"
    manager = NoteManager(note_folder)
    manager.nb_main()
