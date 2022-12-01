"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""


class Code:
    """Translates Hack assembly language mnemonics into binary codes."""

    @staticmethod
    def dest(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a dest mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        if mnemonic == '':
            return "000"
        elif mnemonic == 'M':
            return "001"
        elif mnemonic == "D":
            return "010"
        elif mnemonic == "MD":
            return "011"
        elif mnemonic == "A":
            return "100"
        elif mnemonic == "AM":
            return "101"
        elif mnemonic == "AD":
            return "110"
        elif mnemonic == "AMD":
            return "111"

    @staticmethod
    def comp(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a comp mnemonic string.

        Returns:
            str: 7-bit long binary code of the given mnemonic.
        """
        if mnemonic == '0':
            return "0101010"
        if mnemonic == '1':
            return "0111111"
        if mnemonic == '-1':
            return "0111010"
        if mnemonic == 'D':
            return "0001100"
        if mnemonic == "!D":
            return "0001101"
        if mnemonic == "-D":
            return "0001111"
        if mnemonic == "D+1":
            return "0011111"
        if mnemonic == "D-1":
            return "0001110"
        if mnemonic in ['A', 'M']:
            a = ['A', 'M'].index(mnemonic)
            return str(a) + "110000"
        if mnemonic in ['!A', '!M']:
            a = ['!A', '!M'].index(mnemonic)
            return str(a) + "110001"
        if mnemonic in ["-A", "-M"]:
            a = ["-A", "-M"].index(mnemonic)
            return str(a) + "110011"
        if mnemonic in ["A+1", "M+1"]:
            a = ["A+1", "M+1"].index(mnemonic)
            return str(a) + "110111"
        if mnemonic in ["A-1", "M-1"]:
            a = ["A-1", "M-1"].index(mnemonic)
            return str(a) + "110010"
        if mnemonic in ["D+A", "D+M"]:
            a = ["D+A", "D+M"].index(mnemonic)
            return str(a) + "000010"
        if mnemonic in ["D-A", "D-M"]:
            a = ["D-A", "D-M"].index(mnemonic)
            return str(a) + "010011"
        if mnemonic in ["A-D", "M-D"]:
            a = ["A-D", "M-D"].index(mnemonic)
            return str(a) + "000111"
        if mnemonic in ["D&A", "D&M"]:
            a = ["D&A", "D&M"].index(mnemonic)
            return str(a) + "000000"
        if mnemonic in ["D|A", "D|M"]:
            a = ["D|A", "D|M"].index(mnemonic)
            return str(a) + "010101"

        # additional shift instructions
        if mnemonic == "D<<":
            return "0110000"
        if mnemonic == "A<<":
            return "0100000"
        if mnemonic == "M<<":
            return "1100000"
        if mnemonic == "D>>":
            return "0010000"
        if mnemonic == "A>>":
            return "0000000"
        if mnemonic == "M>>":
            return "1000000"

    @staticmethod
    def jump(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a jump mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        if mnemonic == '':
            return "000"
        elif mnemonic == "JGT":
            return "001"
        elif mnemonic == "JEQ":
            return "010"
        elif mnemonic == "JGE":
            return "011"
        elif mnemonic == "JLT":
            return "100"
        elif mnemonic == "JNE":
            return "101"
        elif mnemonic == "JLE":
            return "110"
        elif mnemonic == "JMP":
            return "111"
