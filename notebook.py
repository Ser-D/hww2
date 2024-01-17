from collections import UserDict
import pickle
import os
from abstract import InterfaceForBooks


class Note:
    """ Клас для представлення нотаток. Один екземпляр класу - одна нотатка, що має такі атрибути як заголовок, тіло нотатки та перелік тегів"""

    def __init__(self, note_title, note_body):
        self.note_title = note_title
        self.note_body = note_body
        self.tags = []

    def add_tag(self, tag):
        self.tags.append(tag)

    def __str__(self):
        return f"Note name: {self.note_title}, note: {self.note_body},  tags: {'; '.join(p for p in self.tags)}"


class Notebook(UserDict, InterfaceForBooks):
    """Клас для представлення нотаток. Один екземпляр класу - одна нотатка, що має такі атрибути як заголовок, тіло нотатки та перелік тегів"""

    def add_note(self, note):
        """метод додавання нотатки"""
        if isinstance(note, Note):
            self.data[note.note_title] = note

    def find_note_tag(self, tag):
        """метод пошуку нотаток по тегу"""
        res = None
        res = []
        for note in self.data.values():
            if tag in note.tags:
                res.append(note)
        return res

    def search(self, query: str):
        """метод пошуку фрагмету у тілі нотатки"""
        results = []
        for note in self.data.values():
            if query.lower() in note.note_body.lower():
                results.append(note)
        return results

    def edit_note(self, title, new_body):
        """метод редагування тіла нотатки за назвою"""
        self.data[title].note_body = new_body

    def delete(self, title):
        """метод видалення нотатки за назвою"""
        self.pop(title, None)

    def show_all(self):
        """метот виводу усіх нотаток у зручному для читання форматі"""
        if len(self.data) != 0:
            for note in self.data:
                print(self.data[note])
        print('Nothing to show')

    def save_to_file(self, file):
        """метод збереження нотатки у файл"""
        with open(file, 'wb') as fh:
            pickle.dump(self.data, fh)

    def load_from_file(self, file):
        """метод завантаження нотаток з файлу"""
        if not os.path.exists(file):
            return
        with open(file, 'rb') as fh:
            self.data = pickle.load(fh)
