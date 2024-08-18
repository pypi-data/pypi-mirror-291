import pytest
from wppcpy import exceptions
from wppcpy.filesystem import File

def test_file_read_successful(tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_content = "This is a test file."
    file_path.write_text(file_content)

    file = File(str(file_path))
    content = file.read()

    assert content == file_content

def test_file_read_exception(mocker):
    mocker.patch("builtins.open", side_effect=Exception("Mocked error"))

    file = File("/non/existent/file.txt")

    with pytest.raises(exceptions.file.FileReadException) as exc_info:
        file.read()

    assert "An error occurred while reading the '/non/existent/file.txt': Mocked error" in str(exc_info.value)
