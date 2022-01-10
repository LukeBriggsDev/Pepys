from datetime import date, datetime
from genericpath import exists
import json
import locale
import shutil
import num2words
import os
import pathlib
import regex
import yaml
from Crypto import Crypto

from CONSTANTS import get_resource


class EntryFile():
    def __init__(self, file_date: date = None) -> None:

        self._crypto = Crypto()
        if file_date is None:
            self._formatted_date = ""
            self._date = None
            self._directory = ""
            self._long_date = ""
            self._filename = ""
            return

        self._date = file_date
        self._formatted_date = file_date.strftime("%Y-%m-%d")
        
        config_file = get_resource("config.json")
        with open(config_file, "r") as file:
            config_dict = json.loads(file.read())
            diary_directory = config_dict["diary_directory"]
            self._flat_structure = ("use_flat_directory_structure" in config_dict) and config_dict["use_flat_directory_structure"]
            encryption_default = ("encrypt_as_default" in config_dict) and config_dict["encrypt_as_default"]
        
        month_directory = os.path.join(diary_directory, str(file_date.year), f"{file_date.month:02}")
        
        self._directory = os.path.join(month_directory, self._formatted_date)
        
         # Backward compatibility with v1.1.1 and before: Consider directory without zero filled months
        if not os.path.exists(self._directory):
            back_compat_directory = os.path.join(diary_directory, str(file_date.year), str(file_date.month))
            if os.path.exists(back_compat_directory):
                self._directory = os.path.join(back_compat_directory, self._formatted_date)

        self._filename = self.__check_for_existing_filename()
        if self._filename:
            # File already exists at the default location
            self._flat_structure = False
        else:
            # Check if file already exists with flat directory structure
            default_directory = self._directory
            self._directory = os.path.join(diary_directory, str(file_date.year))
            self._filename = self.__check_for_existing_filename()
            if self._filename:
                self._flat_structure = True
            else:
                # For a new file select the file location from the settings
                if self._flat_structure == False:
                    self._directory = default_directory
                self._filename = f"{self._formatted_date}.md"
                if encryption_default:
                    self._filename = self._filename + ".crypt"

         # Add ordinal to end of number if it exists
        try:
            day_of_month = num2words(file_date.day, to="ordinal_num", lang=locale.getlocale()[0])
        except (NotImplementedError, TypeError):
            day_of_month = file_date.day
        self._long_date = file_date.strftime(f"%A {day_of_month} %B %Y")


    @property
    def directory(self):
        """The path to the directory of the entry file"""
        return self._directory


    @property 
    def filename(self):
        """The name of the entry file with extension"""
        return self._filename


    @property
    def path(self):
        """The full path to the entry file"""
        return os.path.join(self._directory, self._filename)


    @property
    def date(self):
        return self._date

    @property
    def formatted_date(self):
        return self._formatted_date


    @property
    def long_date(self):
        return self._long_date


    def update(self):
        self.__init__(self.date)

    def is_encrypted(self):
        return self._filename.endswith(".crypt")


    def set_to_unencrypted(self):
        if not self.is_encrypted():
            return

        file_existed = False
        if self.exists():
            file_existed = True
            content = self.get_content()
            prev_path = self.path

        self._filename = self._filename[:-6]
       
        if file_existed:
            self.save(content)
            os.remove(prev_path)


    def set_to_encrypted(self):
        if self.is_encrypted():
            return

        file_existed = False
        if self.exists():
            file_existed = True
            content = self.get_content()
            prev_path = self.path

        self._filename = self._filename + ".crypt"
       
        if file_existed:
            self.save(content)
            os.remove(prev_path)


    def __check_for_existing_filename(self):
        if not self.directory_exists():
            return False

        path = os.path.join(self._directory, f"{self._formatted_date}.md")
        path_encrypted = os.path.join(self._directory, f"{self._formatted_date}.md.crypt")

        if os.path.exists(path):
            return f"{self._formatted_date}.md"

        if os.path.exists(path_encrypted):
            return f"{self._formatted_date}.md.crypt"

        return ""


    def get_header_text(self):
        return '---\n'\
        f'title: {self._long_date}\n'\
        f'date: {self._formatted_date}\n'\
        'tags: []\n'\
        '---\n'


    def get_content(self):
        if not self.exists():
            return ""

        with open(self.path, "r+") as file:
            content = file.read()
            if self.is_encrypted():
                content = self._crypto.decrypt(content)
            return content


    def directory_exists(self):
        if self._directory == "":
            return False
        return os.path.exists(self._directory)


    def exists(self):
        if not self.directory_exists():
            return False
        return os.path.exists(self.path)


    def create_directory(self):
         pathlib.Path(self._directory).mkdir(parents=True, exist_ok=True)


    def save(self, content: str):
        if content == self.get_header_text():
            # No content in the entry except the header text => No save required
            return

        if not self.directory_exists():
            self.create_directory()

        if (self.is_encrypted()):
            content = self._crypto.encrypt(content)
        
        with open(self.path, "w+") as file:
            file.write(content)


    def get_tags(self):
        content = self.get_content()

        try:
            pattern = regex.compile(r"(?<=(^-{3,}\n)).+?(?=-{3,})", regex.DOTALL)
            metadata = regex.search(pattern, content)
            if metadata is not None:
                meta_dict = yaml.safe_load(metadata.group())
            if "tags" in meta_dict.keys():
                return meta_dict["tags"]
        except Exception:
            return {}


    def copy_image(self, image_path):
        """Copies the image to the local diary entry folder and returns the relative path to the copy"""
        if (self._flat_structure):
            image_directory = os.path.join(self._directory, "images")
            pathlib.Path(image_directory).mkdir(parents=True, exist_ok=True)
        else:
            image_directory = self._directory

        shutil.copy(image_path, image_directory)

        if (self._flat_structure):
            return "./images/" + pathlib.Path(image_path).name
        else:
            return "./" + pathlib.Path(image_path).name
        

def get_all_entry_files():
    with open(get_resource("config.json"), "r") as file:
        directory = json.loads(file.read())["diary_directory"]
    files = list(pathlib.Path(directory).rglob("*-*-*.[mM][dD]"))
    files.extend(list(pathlib.Path(directory).rglob("*-*-*.[mM][dD].crypt")))

    ret = list()
    for file in files:
        fn = file.name;
        fn = fn.replace(".crypt", "")
        fn = fn[:-3]
        date = datetime.strptime(fn, "%Y-%m-%d");
        ret.append(EntryFile(date))

    return ret


def get_all_entry_files_in_range(startdate: date, enddate: date):
    diary_entries = get_all_entry_files()
    diary_entries = [entry for entry in diary_entries
                            if startdate <= entry.date <= enddate]
    return diary_entries
