# import sys
import re
import shutil
from pathlib import Path

class FileOrganizer:
    def __init__(self):
        self.JPEG_IMAGES = []
        self.JPG_IMAGES = []
        self.PNG_IMAGES = []
        self.SVG_IMAGES = []
        self.MP3_AUDIO = []
        self.MY_OTHER = []
        self.ARCHIVES = []
        self.REGISTER_EXTENSIONS = {
            'JPEG': self.JPEG_IMAGES,
            'PNG': self.PNG_IMAGES,
            'JPG': self.JPG_IMAGES,
            'SVG': self.SVG_IMAGES,
            'MP3': self.MP3_AUDIO,
            'ZIP': self.ARCHIVES
        }
        self.FOLDERS = []
        self.EXTENSIONS = set()
        self.UNKNOWN = set()

    def get_extension(self, filename: str) -> str:
        return Path(filename).suffix[1:].upper()

    def scan(self, folder: Path) -> None:
        for item in folder.iterdir():
            if item.is_dir():
                if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                    self.FOLDERS.append(item)
                    self.scan(item)
                continue

            ext = self.get_extension(item.name)
            fullname = folder / item.name

            if not ext:
                self.MY_OTHER.append(fullname)
            else:
                try:
                    container = self.REGISTER_EXTENSIONS[ext]
                    self.EXTENSIONS.add(ext)
                    container.append(fullname)
                except KeyError:
                    self.UNKNOWN.add(ext)
                    self.MY_OTHER.append(fullname)

    def normalize(self, name: str) -> str:
        CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
        TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                       "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
        TRANS = {}
        for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
            TRANS[ord(c)] = l
            TRANS[ord(c.upper())] = l.upper()

        t_name = name.translate(TRANS)
        t_name = re.sub(r'\W', '.', t_name)
        return t_name

    def handle_media(self, filename: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / self.normalize(filename.name))

    def handle_other(self, filename: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / self.normalize(filename.name))

    def handle_archive(self, filename: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        folder_for_file = target_folder / self.normalize(filename.name.replace(filename.suffix, ''))
        folder_for_file.mkdir(exist_ok=True, parents=True)

        try:
            shutil.unpack_archive(str(filename.resolve()), str(folder_for_file.resolve()))
        except shutil.ReadError:
            print(f'Це не архів {filename}!')
            folder_for_file.rmdir()
            return None

        filename.unlink()

    def handle_folder(self, folder: Path):
        try:
            folder.rmdir()
        except OSError:
            print(f'Помилка видалення папки {folder}')

    def organize_files(self, folder: Path):
        self.scan(folder)

        for file in self.JPEG_IMAGES:
            self.handle_media(file, folder / 'images' / 'JPEG')
        for file in self.JPG_IMAGES:
            self.handle_media(file, folder / 'images' / 'JPG')
        for file in self.PNG_IMAGES:
            self.handle_media(file, folder / 'images' / 'PNG')
        for file in self.SVG_IMAGES:
            self.handle_media(file, folder / 'images' / 'SVG')
        for file in self.MP3_AUDIO:
            self.handle_media(file, folder / 'audio' / 'MP3')
        for file in self.MY_OTHER:
            self.handle_other(file, folder / 'MY_OTHER')
        for file in self.ARCHIVES:
            self.handle_archive(file, folder / 'archives')

        for folder in self.FOLDERS[::-1]:
            self.handle_folder(folder)

def start(folder_path):
    folder_for_scan = Path(folder_path)
    print(f'Start in folder {folder_for_scan.resolve()}')
    file_organizer = FileOrganizer()
    file_organizer.organize_files(folder_for_scan.resolve())
