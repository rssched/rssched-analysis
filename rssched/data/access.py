import importlib.resources as resources
from pathlib import Path


class PkgDataAccess:
    def __init__(self) -> None:
        pass

    @staticmethod
    def locate_request() -> Path:
        data_folder = resources.files("rssched.data")
        file_path = data_folder / "example.instance.scheduler_request.json"
        return file_path

    @staticmethod
    def locate_response() -> Path:
        data_folder = resources.files("rssched.data")
        file_path = data_folder / "example.instance.scheduler_response.json"
        return file_path
