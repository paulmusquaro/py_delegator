import os


class NoteManager:
    def __init__(self, note_folder):
        self.note_folder = note_folder

    def create_note(self, title, content, tags):
        note_path = os.path.join(self.note_folder, f"{title}.txt")
        with open(note_path, "w") as file:
            file.write(f"Title: {title}\n")
            file.write(f"Content: {content}\n")
            file.write(f"Tags: {', '.join(tags)}\n")

    def search_notes_by_tags(self, tags):
        matching_notes = []
        for filename in os.listdir(self.note_folder):
            if filename.endswith(".txt"):
                with open(os.path.join(self.note_folder, filename), "r") as file:
                    content = file.read()
                    if all(tag in content for tag in tags):
                        matching_notes.append(content)

        if matching_notes:
            print(f"Notes containing tags {tags}")
            for note in matching_notes:
                print("-" * 20)
                print(note)
        else:
            print(f"No notes with tags {tags} were found")

    def search_notes_by_title(self, title):
        matching_notes = []
        for filename in os.listdir(self.note_folder):
            if filename.endswith(".txt") and title in filename:
                note_path = os.path.join(self.note_folder, filename)
                with open(note_path, "r") as file:
                    note_content = file.read()
                    matching_notes.append(note_content)

        if matching_notes:
            print(f"Notes, by name {title}")
            for note in matching_notes:
                print("-" * 20)
                print(note)
        else:
            print(f"No notes with title {title} found")

    def display_all_notes(self):
        for filename in os.listdir(self.note_folder):
            if filename.endswith(".txt"):
                note_path = os.path.join(self.note_folder, filename)
                with open(note_path, "r") as file:
                    note_content = file.read()
                    print(note_content)
                    print("-" * 20)

    def edit_note(self, title, new_content):
        note_path = os.path.join(self.note_folder, f"{title}.txt")
        if os.path.exists(note_path):
            with open(note_path, "w") as file:
                file.write(f"Title: {title}\n")
                file.write(f"Content: {new_content}\n")

    def delete_note(self, title):
        note_path = os.path.join(self.note_folder, f"{title}.txt")
        if os.path.exists(note_path):
            os.remove(note_path)

    def nb_main(self):

        if not os.path.exists(self.note_folder):
            os.makedirs(self.note_folder)

        while True:
            print("\nMenu:")
            print("1. Create a note")
            print("2. Search notes by tags")
            print("3. Search for notes by name")
            print("4. Show all notes")
            print("5. Edit note")
            print("6. Delete note")
            print("7. Exit")

            choice = input("Select an option: ")

            if choice == "1":
                title = input("Enter a name for the note:")
                content = input("Enter the content of the note:")
                tags = input("Enter tags (through commas): ").split(", ")
                self.create_note(title, content, tags)
                print("Note created.")

            elif choice == "2":
                tags_to_search = input("Enter tags to search (through commas): ").split(", ")
                self.search_notes_by_tags(tags_to_search)

            elif choice == "3":
                title_to_search = input("Enter a name to search for: ")
                self.search_notes_by_title(title_to_search)

            elif choice == "4":
                print("\n" + ("-" * 20))
                self.display_all_notes()

            elif choice == "5":
                title = input("Enter the name of the note to edit: ")
                new_content = input("Enter the new content of the note:")
                self.edit_note(title, new_content)
                print("The note has been updated.")

            elif choice == "6":
                title = input("Enter the name of the note to delete: ")
                self.delete_note(title)
                print("Note deleted.")

            elif choice == "7":
                break

            else:
                print("Wrong choice. Please select the correct option.")


if __name__ == "__main__":
    """

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
