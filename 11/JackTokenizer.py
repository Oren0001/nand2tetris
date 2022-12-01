"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import typing


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    """

    LINE_COMMENT = "//"
    COMMENT_START = "/*"
    COMMENT_END = "*/"
    TOKEN_TYPES = ("keyword", "symbol", "integerConstant", "stringConstant",
                   "identifier")
    KEYWORDS = ('class', 'constructor', 'function', 'method', 'field',
                'static', 'var', 'int', 'char', 'boolean', 'void',
                'true', 'false', 'null', 'this', 'let', 'do', 'if',
                'else', 'while', 'return')
    SYMBOLS = ('{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '=', '*',
               '/', '&', '|', '<', '>', '-', '~', '^', '#')

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        # Your code goes here!
        # A good place to start is:
        # input_lines = input_stream.read().splitlines()
        self._token_type_pairs = list()
        self.fetch_tokens(input_stream)
        self._cur = 0

    def fetch_tokens(self, input_stream: typing.TextIO) -> None:
        """
        Adds all tokens to the data member _tokens.
        No whitespaces, new line characters and comments will be added.
        """
        while True:
            line = input_stream.readline()
            # end of file?
            if not line:
                return
            # remove start and end whitespaces and '\n'
            line = line.strip()
            # skip comments
            if line.startswith(self.COMMENT_START):
                while not line.endswith(self.COMMENT_END):
                    line = input_stream.readline().strip()
                continue
            i = 0
            n = len(line)
            while i < n:
                # skip whitespaces
                if line[i].isspace():
                    i += 1
                    continue
                # skip comment '//'
                if (i + 1 < n) and line[i:i + 2] == self.LINE_COMMENT:
                    break
                # skip comment '/* ... */'
                if (i + 1 < n) and line[i:i + 2] == self.COMMENT_START:
                    end = (i + 2) + line[i + 2:].find('*/') + 1
                    i = end + 1
                    continue
                # add string constant
                if line[i] == '"':
                    end = (i + 1) + line[i + 1:].index('"')
                    self._token_type_pairs.append((line[i:end + 1], self.TOKEN_TYPES[3]))
                    i = end + 1
                    continue
                # add integer constant
                if line[i].isdecimal():
                    end = i + 1
                    while (end < n) and line[end].isdecimal():
                        end += 1
                    self._token_type_pairs.append((line[i:end], self.TOKEN_TYPES[2]))
                    i = end
                    continue
                # add symbols
                if line[i] in self.SYMBOLS:
                    self._token_type_pairs.append((line[i], self.TOKEN_TYPES[1]))
                    i += 1
                    continue
                # add keywords
                for keyword in self.KEYWORDS:
                    m = len(keyword)
                    keyword_suffix = line[i + m] if (i + m < n) else str()
                    if line[i:].startswith(keyword) and (
                            keyword_suffix in self.SYMBOLS or keyword_suffix.isspace()
                            or i + m == n):
                        self._token_type_pairs.append((keyword, self.TOKEN_TYPES[0]))
                        i += len(keyword)
                        break
                else:  # identifier
                    end = i + 1
                    while (end < n) and (
                            line[end] == '_' or line[end].isalnum()):
                        end += 1
                    self._token_type_pairs.append((line[i:end], self.TOKEN_TYPES[4]))
                    i = end
                    continue

    def get_token_type_pairs(self):
        return self._token_type_pairs
