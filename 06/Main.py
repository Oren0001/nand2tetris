"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code

C_COMMAND = "111"
SHIFT_COMMAND = "101"


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # initialize
    symbol_table = SymbolTable()
    parser = Parser(input_file)
    c_converter = Code()

    # first pass
    label_num = 0
    while parser.has_more_commands():
        if parser.command_type() == parser.COMMANDS[2]:
            symbol_table.add_entry(
                parser.symbol(), parser.get_command_num() - label_num)
            label_num += 1
        parser.advance()

    # second pass
    var_address = symbol_table.PRESERVED_REGISTERS_NUM
    while parser.has_more_commands():
        if parser.command_type() == parser.COMMANDS[0]:
            symbol = parser.symbol()
            if symbol_table.contains(symbol):
                output_file.write(
                    '{0:016b}'.format(symbol_table.get_address(symbol)) + '\n')
            else:
                try:
                    register_address = int(symbol)
                    output_file.write('{0:016b}'.format(register_address) +
                                      '\n')
                except ValueError:
                    symbol_table.add_entry(symbol, var_address)
                    output_file.write('{0:016b}'.format(var_address) + '\n')
                    var_address += 1
        elif parser.command_type() == parser.COMMANDS[1]:
            comp = c_converter.comp(parser.comp())
            dest = c_converter.dest(parser.dest())
            jump = c_converter.jump(parser.jump())
            op = SHIFT_COMMAND if parser.is_shift() else C_COMMAND
            output_file.write(op + comp + dest + jump + '\n')
        parser.advance()


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
