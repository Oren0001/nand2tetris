"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """
    KINDS = ("static", "field", "argument", "var")

    class TableEntry:
        def __init__(self, name, type_, kind, index) -> None:
            self._name = name
            self._type = type_
            self._kind = kind
            self._index = index

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        self._class_table = dict()
        self._field_counter = 0
        self._static_counter = 0

        self._subroutine_table = dict()
        self._arg_counter = 0
        self._var_counter = 0

        self._class_name = ''

    def start_subroutine(self, is_method) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's
        symbol table).
        """
        self._subroutine_table = dict()
        self._arg_counter = 1 if is_method else 0
        self._var_counter = 0

    def define(self, name: str, type_: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns
        it a running index. "STATIC" and "FIELD" identifiers have a class
        scope, while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type_ (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        if kind == self.KINDS[0]:
            index = self._static_counter
            self._static_counter += 1
        elif kind == self.KINDS[1]:
            kind = "this"
            index = self._field_counter
            self._field_counter += 1
        elif kind == self.KINDS[2]:
            index = self._arg_counter
            self._arg_counter += 1
        else:
            kind = "local"
            index = self._var_counter
            self._var_counter += 1
        new_entry = SymbolTable.TableEntry(name, type_, kind, index)
        if kind == "static" or kind == "this":
            self._class_table[name] = new_entry
        elif kind == "argument" or kind == "local":
            self._subroutine_table[name] = new_entry

    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in
            the current scope.
        """
        if kind == self.KINDS[0]:
            return self._static_counter
        elif kind == self.KINDS[1]:
            return self._field_counter
        elif kind == self.KINDS[2]:
            return self._arg_counter
        else:
            return self._var_counter

    def kind_of(self, name: str):
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or
            None if the identifier is unknown in the current scope.
        """
        if self._subroutine_table.get(name):
            return self._subroutine_table[name]._kind
        elif self._class_table.get(name):
            return self._class_table[name]._kind
        else:
            return None

    def type_of(self, name: str):
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        if self._subroutine_table.get(name):
            return self._subroutine_table[name]._type
        elif self._class_table.get(name):
            return self._class_table[name]._type
        else:
            return None

    def index_of(self, name: str):
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        if self._subroutine_table.get(name):
            return self._subroutine_table[name]._index
        elif self._class_table.get(name):
            return self._class_table[name]._index
        else:
            return None

    def get_class_name(self):
        return self._class_name

    def set_class_name(self, name):
        self._class_name = name
