import pytest
from cli.parser import parser
from cli.parser import read_args
from cli.parser import read_file
import argparse


def test_parser(monkeypatch):
    monkeypatch.setattr('sys.argv', ['parser.py', '--string', "abcd"])

    args = parser()
    result_var = read_args(args)[1]
    assert result_var == "abcd"


@pytest.fixture
def create_test_file(tmpdir):
    file_path = tmpdir.join("test_file.txt")
    with open(file_path, 'w') as test_file:
        test_file.write("abcdef")
    return file_path


def test_read_file(create_test_file):
    result_var = read_file(create_test_file)
    assert result_var == "abcdef"


@pytest.mark.parametrize(
    "args, output",
    [
        (argparse.Namespace(string='abc', file=None), (False, "abc")),
        (argparse.Namespace(string=None, file="path/to/file"), (True, "path/to/file")),
        (argparse.Namespace(string='abc', file="path/to/file"), (True, "path/to/file"))
    ]
)
def test_read_args(args, output):
    result = read_args(args)
    assert result == output


if __name__ == '__main__':
    pytest.main()
