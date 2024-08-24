import os

from boj.errors.error import FileIOError


def mkdir(path: str, exist_ok=True):
    try:
        os.makedirs(name=path, exist_ok=exist_ok)
    except OSError as e:
        raise e


def file_exists(path: str):
    if os.path.isfile(path):
        return True
    return False


class GeneralFileIO:
    def read(self, path: str) -> bytes:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"'{path}' is not a file or does not exist")

        try:
            with open(path, "rb") as file:
                data = file.read()

            return data
        except Exception:
            raise FileIOError(f"Error while reading the file '{path}'")

    def write(self, raw: bytes, path: str) -> None:
        mkdir(os.path.dirname(path))
        with open(path, "wb") as file:
            file.write(raw)
