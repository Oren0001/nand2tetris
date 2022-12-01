"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.
    """

    COMMENT = "//"
    ARITHMETIC_COMMAND = "C_ARITHMETIC"
    SHIFT_COMMAND_PREFIX = "shift"
    NON_ARITHMETIC_C_COMMANDS = ("C_PUSH", "C_POP", "C_LABEL", "C_GOTO",
                                 "C_IF", "C_FUNCTION", "C_CALL", "C_RETURN",
                                 "C_SHIFT")
    NON_ARITHMETIC_COMMANDS = {"push": "C_PUSH", "pop": "C_POP",
                               "label": "C_LABEL", "goto": "C_GOTO",
                               "if-goto": "C_IF", "function": "C_FUNCTION",
                               "return": "C_RETURN", "call": "C_CALL"}

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is:
        # input_lines = input_file.read().splitlines()
        self._commands = list()
        self.fetch_commands(input_file)
        self._cur = 0

    def fetch_commands(self, input_file: typing.TextIO) -> None:
        """
        Adds all the commands to the data member _commands.
        No whitespaces, new line characters and comments will be added.
        """
        for line in input_file:
            i = line.find(self.COMMENT)
            if i != -1:
                line = line[:i]  # remove comments
            line = line.strip()  # remove start and end whitespaces and '\n'
            if len(line) == 0:
                continue
            else:
                self._commands.append(line.split(' '))

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self._cur < len(self._commands)

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true.
        Initially there is no current command.
        """
        self._cur += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        command = self._commands[self._cur]
        if command[0].startswith(self.SHIFT_COMMAND_PREFIX):
            return self.NON_ARITHMETIC_C_COMMANDS[-1]
        elif self.NON_ARITHMETIC_COMMANDS.get(command[0]):
            return self.NON_ARITHMETIC_COMMANDS[command[0]]
        else:
            return self.ARITHMETIC_COMMAND

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        return self._commands[self._cur][0]

    def arg2(self) -> str:
        """
        Returns:
            str: the second argument of the current command. Should not
            be called if the current command is "C_ARITHMETIC" or "C_RETURN".
        """
        return self._commands[self._cur][1]

    def arg3(self) -> str:
        """
        Returns:
            int: the third argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP",
            "C_FUNCTION" or "C_CALL".
        """
        return self._commands[self._cur][2]
