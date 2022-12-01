"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""


class SymbolTable:
    """
    A symbol table that keeps a correspondence between symbolic labels and 
    numeric addresses.
    """
    PRESERVED_REGISTERS_NUM = 16
    SCREEN = 16384
    KBD = 24576
    SP = 0
    LCL = 1
    ARG = 2
    THIS = 3
    THAT = 4

    def __init__(self) -> None:
        """Creates a new symbol table initialized with all the predefined
        symbols and their pre-allocated RAM addresses, according to
        6.2.3 of the book.
        """
        self._table = dict()
        self.initialize_table()

    def initialize_table(self) -> None:
        """
        Adds all the predefined symbols to the table.
        """
        for i in range(self.PRESERVED_REGISTERS_NUM):
            self._table['R' + str(i)] = i
        self._table["SCREEN"] = self.SCREEN
        self._table["KBD"] = self.KBD
        self._table["SP"] = self.SP
        self._table["LCL"] = self.LCL
        self._table["ARG"] = self.ARG
        self._table["THIS"] = self.THIS
        self._table["THAT"] = self.THAT

    def add_entry(self, symbol: str, address: int) -> None:
        """Adds the pair (symbol, address) to the table.

        Args:
            symbol (str): the symbol to add.
            address (int): the address corresponding to the symbol.
        """
        self._table[symbol] = address

    def contains(self, symbol: str) -> bool:
        """Does the symbol table contain the given symbol?

        Args:
            symbol (str): a symbol.

        Returns:
            bool: True if the symbol is contained, False otherwise.
        """
        return False if (self._table.get(symbol) is None) else True

    def get_address(self, symbol: str) -> int:
        """Returns the address associated with the symbol.

        Args:
            symbol (str): a symbol.

        Returns:
            int: the address associated with the symbol.
                 -1 if the table doesn't contain the symbol.
        """
        address = self._table.get(symbol)
        return address if (address is not None) else -1
