from datetime import date
from genericpath import exists
import json
import locale
import shutil
import num2words
import os
import pathlib
import regex
import yaml

from CONSTANTS import get_resource


class EntryFile():
    def __init__(self, file_date: date = None) -> None:

        if file_date is None:
            self._formatted_date = ""
            self._directory = ""
            self._long_date = ""
            return

        self._formatted_date = file_date.strftime("%Y-%m-%d")
        
        config_file = get_resource("config.json")
        with open(config_file, "r") as file:
            diary_directory = json.loads(file.read())["diary_directory"]
            month_directory = os.path.join(diary_directory, str(file_date.year), f"{file_date.month:02}")
        
        self._directory = os.path.join(month_directory, self._formatted_date)
        
         # Backward compatibility with v1.1.1 and before: Consider directory without zero filled months
        if not os.path.exists(self._directory):
            back_compat_directory = os.path.join(diary_directory, str(file_date.year), str(file_date.month))
            if os.path.exists(back_compat_directory):
                self._directory = os.path.join(back_compat_directory, self._formatted_date)

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
    def path(self):
        """The full path to the entry file"""
        return os.path.join(self._directory, f"{self._formatted_date}.md")


    @property
    def formatted_date(self):
        return self._formatted_date

    @property
    def long_date(self):
        return self._long_date

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
                return file.read()

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
        shutil.copy(image_path, self._directory)
        return "./" + pathlib.Path(image_path).name

def get_all_entry_files():
    with open(get_resource("config.json"), "r") as file:
        directory = json.loads(file.read())["diary_directory"]
    return list(pathlib.Path(directory).rglob("*-*-*.[mM][dD]"))

def get_all_entry_files_in_range(startdate: date, enddate: date):
    diary_entries = get_all_entry_files()
    diary_entries = [entry for entry in diary_entries
                            if startdate.strftime("%Y-%m-%d") <= entry.name[:-3] <= enddate.strftime("%Y-%m-%d")]
    return diary_entries
