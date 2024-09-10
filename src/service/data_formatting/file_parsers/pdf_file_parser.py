from pdfminer.high_level import extract_text
from src.service.data_formatting.file_parsers.file_parser import FileParser


class PdfFileParser(FileParser):
    _EXTENSION = ".pdf"

    def _parse_file(self) -> str:
        with open(self._filepath, mode="rb") as fin:

            text = extract_text(fin)
            
            return text

