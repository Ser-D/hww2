from abc import ABC, abstractmethod


class InterfaceForBooks(ABC):
    """Абстрактний клас для адресної книги та книги нотатків"""

    @abstractmethod
    def show_all(self):
        pass

    @abstractmethod
    def save_to_file(self, file):
        pass

    @abstractmethod
    def load_from_file(self, file):
        pass