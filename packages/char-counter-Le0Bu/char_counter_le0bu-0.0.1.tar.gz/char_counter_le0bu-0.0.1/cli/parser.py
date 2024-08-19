import argparse
from char_counter.char_counter import count
from typing import Tuple


# Args input should be result of Parser func with custom
# .file and .string attributes
def read_args(args) -> Tuple[bool, str]:
    if args.file is not None:
        return True, args.file
    elif args.string is not None:
        return False, args.string


def read_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# Returns data only for read_args function to read.
def parser():
    parser_var = argparse.ArgumentParser()
    parser_var.add_argument('--string', type=str, help='String to count lonely characters')
    parser_var.add_argument('--file', type=str, help='Path to file, in which we count')
    return parser_var.parse_args()


# In theory, I can change bool/None to options list if I'll need more than 2 --flags
def main_logic():
    args = read_args(parser())
    if args is None:
        result = "Required arguments were not provided"
    elif args[0]:
        try:
            result = count(read_file(args[1]))
        except FileNotFoundError:
            result = "File not found"
        except (OSError, UnicodeDecodeError):
            result = "Unable to read the file"
    elif not args[0]:
        result = count(args[1])

    print(result)


if __name__ == "__main__":
    main_logic()
