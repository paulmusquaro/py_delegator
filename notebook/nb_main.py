import os

# Шлях до папки для зберігання нотаток
note_folder = "notebook/notes"


# Функція для створення нової нотатки
def create_note(title, content, tags):
    note_path = os.path.join(note_folder, f"{title}.txt")
    with open(note_path, "w") as file:
        file.write(f"Заголовок: {title}\n")
        file.write(f"Зміст: {content}\n")
        file.write(f"Теги: {', '.join(tags)}\n")


# Функція для пошуку нотаток за ключовими словами (тегами)
def search_notes_by_tags(tags):
    matching_notes = []
    for filename in os.listdir(note_folder):
        if filename.endswith(".txt"):
            with open(os.path.join(note_folder, filename), "r") as file:
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


# Функція для пошуку нотаток за назвою та виведення всієї інформації
def search_notes_by_title(title):
    matching_notes = []
    for filename in os.listdir(note_folder):
        if filename.endswith(".txt") and title in filename:
            note_path = os.path.join(note_folder, filename)
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


# Функція для відображення всіх нотаток
def display_all_notes():
    for filename in os.listdir(note_folder):
        if filename.endswith(".txt"):
            note_path = os.path.join(note_folder, filename)
            with open(note_path, "r") as file:
                note_content = file.read()
                print(note_content)
                print("-" * 20)  # Розділювач між нотатками


# Функція для редагування нотатки
def edit_note(title, new_content):
    note_path = os.path.join(note_folder, f"{title}.txt")
    if os.path.exists(note_path):
        with open(note_path, "w") as file:
            file.write(f"Заголовок: {title}\n")
            file.write(f"Зміст: {new_content}\n")


# Функція для видалення нотатки
def delete_note(title):
    note_path = os.path.join(note_folder, f"{title}.txt")
    if os.path.exists(note_path):
        os.remove(note_path)


# Текстове меню
def nb_main():
    # Переконайтеся, що папка для зберігання нотаток існує
    if not os.path.exists(note_folder):
        os.makedirs(note_folder)

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
            create_note(title, content, tags)
            print("Нотатка створена.")

        elif choice == "2":
            tags_to_search = input("Введіть теги для пошуку (через кому): ").split(", ")
            search_notes_by_tags(tags_to_search)

        elif choice == "3":
            title_to_search = input("Введіть назву для пошуку: ")
            search_notes_by_title(title_to_search)

        elif choice == "4":
            print("\n" + ("-" * 20))
            display_all_notes()

        elif choice == "5":
            title = input("Введіть назву нотатки для редагування: ")
            new_content = input("Введіть новий зміст нотатки: ")
            edit_note(title, new_content)
            print("Нотатка оновлена.")

        elif choice == "6":
            title = input("Введіть назву нотатки для видалення: ")
            delete_note(title)
            print("Нотатка видалена.")

        elif choice == "7":
            break

        else:
            print("Невірний вибір. Будь ласка, виберіть коректну опцію.")
