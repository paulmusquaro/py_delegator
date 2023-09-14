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
        self.JFIF_IMAGES = []
        self.AVI_VIDEO = []
        self.MP4_VIDEO = []
        self.MOV_VIDEO = []
        self.MKV_VIDEO = []
        self.DOC_DOCUMENTS = []
        self.DOCX_DOCUMENTS = []
        self.TXT_DOCUMENTS = []
        self.PDF_DOCUMENTS = []
        self.XLSX_DOCUMENTS = []
        self.PPTX_DOCUMENTS = []
        self.MP3_AUDIO = []
        self.OGG_AUDIO = []
        self.WAV_AUDIO = []
        self.AMR_AUDIO = []
        self.ZIP_ARCHIVES = []
        self.GZ_ARCHIVES = []
        self.TAR_ARCHIVES = []
        self.MY_OTHER = []
        self.REGISTER_EXTENSIONS = {
            'JPEG':self.JPEG_IMAGES,
            'JPG':self.JPG_IMAGES,
            'PNG':self.PNG_IMAGES,
            'SVG':self.SVG_IMAGES,
            'JFIF':self.JFIF_IMAGES,
            'AVI':self.AVI_VIDEO,
            'MP4':self.MP4_VIDEO,
            'MOV':self.MOV_VIDEO,
            'MKV':self.MKV_VIDEO,
            'DOC':self.DOC_DOCUMENTS,
            'DOCX':self.DOCX_DOCUMENTS,
            'TXT':self.TXT_DOCUMENTS,
            'PDF':self.PDF_DOCUMENTS,
            'XLSX':self.XLSX_DOCUMENTS,
            'PPTX':self.PPTX_DOCUMENTS,
            'MP3':self.MP3_AUDIO,
            'OGG':self.OGG_AUDIO,
            'WAV':self.WAV_AUDIO,
            'AMR':self.AMR_AUDIO,
            'ZIP':self.ZIP_ARCHIVES,
            'GZ':self.GZ_ARCHIVES,
            'TAR':self.TAR_ARCHIVES}
        

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
        for file in self.JFIF_IMAGES:
            self.handle_media(file, folder / 'images' / 'JFIF')

        for file in self.AVI_VIDEO:
            self.handle_media(file, folder / 'video' / 'AVI')
        for file in self.MP4_VIDEO:
            self.handle_media(file, folder / 'video' / 'MP4')
        for file in self.MOV_VIDEO:
            self.handle_media(file, folder / 'video' / 'MOV')
        for file in self.MKV_VIDEO:
            self.handle_media(file, folder / 'video' / 'MKV')

        for file in self.DOC_DOCUMENTS:
            self.handle_media(file, folder / 'documents' / 'DOC')
        for file in self.DOCX_DOCUMENTS:
            self.handle_media(file, folder / 'documents' / 'DOCX')
        for file in self.TXT_DOCUMENTS:
            self.handle_media(file, folder / 'documents' / 'TXT')
        for file in self.PDF_DOCUMENTS:
            self.handle_media(file, folder / 'documents' / 'PDF')
        for file in self.XLSX_DOCUMENTS:
            self.handle_media(file, folder / 'documents' / 'XLSX')
        for file in self.PPTX_DOCUMENTS:
            self.handle_media(file, folder / 'documents' / 'PPTX')

        for file in self.MP3_AUDIO:
            self.handle_media(file, folder / 'audio' / 'MP3')
        for file in self.OGG_AUDIO:
            self.handle_media(file, folder / 'audio' / 'OGG')
        for file in self.WAV_AUDIO:
            self.handle_media(file, folder / 'audio' / 'WAV')
        for file in self.AMR_AUDIO:
            self.handle_media(file, folder / 'audio' / 'AMR')

        for file in self.ZIP_ARCHIVES:
            self.handle_archive(file, folder / 'archives' / 'ZIP')
        for file in self.GZ_ARCHIVES:
            self.handle_archive(file, folder / 'archives' / 'GZ')
        for file in self.TAR_ARCHIVES:
            self.handle_archive(file, folder / 'archives' / 'TAR')

        for file in self.MY_OTHER:
            self.handle_other(file, folder / 'MY_OTHER')

        for folder in self.FOLDERS[::-1]:
            self.handle_folder(folder)

def start(folder_path):
    folder_for_scan = Path(folder_path)
    print(f'Start in folder {folder_for_scan.resolve()}')
    file_organizer = FileOrganizer()
    file_organizer.organize_files(folder_for_scan.resolve())
