# coding=utf-8
"""
Convert a text file to ascii

Usage:
  convertfile_ascii [options] <filepath>

Options:
  -h --help     Show this screen.

author  : rabshakeh (erik@a8.nl)
project : consoleprinter
created : 10-11-15 / 17:31
"""
import sys

from arguments import Arguments
from consoleprinter import transliterate, forceascii, console

if sys.version_info.major < 3:
    console("\033[31mpython3 is required\033[0m")
    exit(1)


class IArguments(Arguments):
    """
    IArguments
    """
    def __init__(self, doc):
        """
        __init__
        """
        self.help = False
        self.filepath = ""
        super().__init__(doc)


def main():
    """
    main
    """
    arguments = IArguments(__doc__)
    content = open(arguments.filepath).read()
    open(arguments.filepath + ".bak", "w").write(content)
    try:
        newcontent = transliterate(content)
    except UnicodeEncodeError as ex:
        console(str(ex), color="red")
        newcontent = forceascii(content)

    open(arguments.filepath, "w").write(newcontent)


if __name__ == "__main__":
    main()
