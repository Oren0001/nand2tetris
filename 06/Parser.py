"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads and assembly language 
    command, parses it, and provides convenient access to the commands 
    components (fields and symbols). In addition, removes all white space and 
    comments.
    """

    COMMENT = "//"
    COMMANDS = ("A_COMMAND", "C_COMMAND", "L_COMMAND")
    A_PREFIX = '@'
    L_PREFIX = '('
    L_SUFFIX = ')'
    C_SEPARATORS = ('=', ';')
    SHIFT_LEFT = "<<"
    SHIFT_RIGHT = ">>"

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        self._commands = list()
        self.fetch_commands(input_file)
        self._cur = 0  # index of current command

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
            line = line.replace(' ', '')  # remove inner whitespaces
            if len(line) == 0:
                continue
            else:
                self._commands.append(line)

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            if there are more commands, return True.
            else, resets the command number to 0, and returns False.
        """
        if self._cur < len(self._commands):
            return True
        else:
            self._cur = 0
            return False

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current
        command. Should be called only if has_more_commands() is true.
        """
        self._cur += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a
                        decimal number.
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx
                        is a symbol.
        """
        if self._commands[self._cur][0] == self.A_PREFIX:
            return self.COMMANDS[0]
        elif self._commands[self._cur][0] == self.L_PREFIX:
            return self.COMMANDS[2]
        else:
            return self.COMMANDS[1]

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        if self._commands[self._cur][-1:] == self.L_SUFFIX:
            return self._commands[self._cur][1:-1]
        else:
            return self._commands[self._cur][1:]

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        equals_index = self._commands[self._cur].find(self.C_SEPARATORS[0])
        if equals_index != -1:
            return self._commands[self._cur][:equals_index].rstrip()
        else:
            return ''

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        equals_index = self._commands[self._cur].find(self.C_SEPARATORS[0])
        semicolon_index = self._commands[self._cur].find(self.C_SEPARATORS[1])
        if (equals_index != -1) and (semicolon_index != -1):
            return self._commands[self._cur][
                   equals_index + 1:semicolon_index].strip()
        if (equals_index != -1) and (semicolon_index == -1):
            return self._commands[self._cur][equals_index + 1:].strip()
        if (equals_index == -1) and (semicolon_index != -1):
            return self._commands[self._cur][:semicolon_index].strip()
        else:
            return self._commands[self._cur]

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        semicolon_index = self._commands[self._cur].find(self.C_SEPARATORS[1])
        if semicolon_index != -1:
            return self._commands[self._cur][semicolon_index + 1:].lstrip()
        else:
            return ''

    def get_command_num(self) -> int:
        """
        Returns the current command number.
        """
        return self._cur

    def is_shift(self) -> bool:
        """
        Returns True if the command consists shift, otherwise False.
        """
        return True if (self.SHIFT_LEFT in self._commands[self._cur] or
                        self.SHIFT_RIGHT in self._commands[self._cur]) \
            else False
