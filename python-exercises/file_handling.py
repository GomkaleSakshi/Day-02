"""Write to and read from a temporary text file."""

from pathlib import Path
from tempfile import TemporaryDirectory


with TemporaryDirectory() as temporary_directory:
    file_path = Path(temporary_directory) / "example.txt"
    file_path.write_text("Python can read and write files.\n", encoding="utf-8")
    print(file_path.read_text(encoding="utf-8"), end="")