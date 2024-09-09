from pdf2txt import PdfDocument

from src.service.data_formatting.file_parsers.file_parser import FileParser


class PdfFileParser(FileParser):
    _EXTENSION = ".pdf"

    def _parse_file(self) -> str:
        with open(self._filepath, mode="rb", encoding="utf-8") as fin:
            doc = PdfDocument(fin)
            # TODO: разобраться как достать текст
            raise NotImplementedError()
