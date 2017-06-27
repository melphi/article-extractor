from os.path import join, dirname, realpath
from json import loads

from app.modules.extractor.models import PageRaw


class FileUtils(object):
    @staticmethod
    def read_text(resource_file_name: str) -> str:
        file_path = FileUtils._get_file_path(resource_file_name)
        with open(file_path) as file:
            return file.read()

    @staticmethod
    def read_json(resource_file_name: str) -> dict:
        data = FileUtils.read_text(resource_file_name)
        return loads(data)

    @staticmethod
    def _get_file_path(file_name: str) -> str:
        return join(dirname(realpath(__file__)), file_name)
