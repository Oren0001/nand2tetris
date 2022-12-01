"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from CompilationEngine import CompilationEngine
from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter


def add_vars_to_symbol_table(_input, i, symbol_table):
    if _input[i][0] == "<classVarDec>" or _input[i][0] == "<varDec>":
        i += 1
        while (_input[i][0] != "</classVarDec>") and (_input[i][0] != "</varDec>"):
            kind = _input[i][1]
            _type = _input[i + 1][1]
            i += 2
            while _input[i][1] != ';':
                if _input[i][0] == "identifier":
                    name = _input[i][1]
                    symbol_table.define(name, _type, kind)
                i += 1
            i += 1
        return i
    elif _input[i][0] == "<parameterList>":
        i += 1
        kind = "argument"
        while _input[i][0] != "</parameterList>":
            if _input[i][0] != "symbol":
                _type = _input[i][1]
                i += 1
                name = _input[i][1]
                symbol_table.define(name, _type, kind)
            i += 1
        return i
    else:
        return i


def compile_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Compiles a single file.

    Args:
        input_file (typing.TextIO): the file to compile.
        output_file (typing.TextIO): writes all output to this file.
    """
    _input = list()
    tokenizer = JackTokenizer(input_file)
    engine = CompilationEngine(tokenizer.get_token_type_pairs(), _input)
    engine.compile_class()
    symbol_table = SymbolTable()
    vm_writer = VMWriter(output_file, symbol_table, engine.get_methods_names())
    symbol_table.set_class_name(_input[2][1])

    temp_name = str()
    function_type = str()
    is_void = bool()
    i = 4
    while i < len(_input):
        # update symbol table
        temp = i
        i = add_vars_to_symbol_table(_input, i, symbol_table)
        if i != temp:
            continue
        # write statements
        elif type(_input[i][0]) == str and _input[i][0].endswith("Statement>"):
            vm_writer.write_statements(_input[i][0], _input[i + 1])
            i += 3
        # write subroutine declarations
        elif type(_input[i][0]) == str and _input[i][0] == "<subroutineDec>":
            function_type = _input[i + 1][1]
            is_void = (_input[i + 2][1] == "void")
            temp_name = _input[i + 3][1]
            symbol_table.start_subroutine(function_type == "method")
            i += 5
        elif _input[i][0] == "<subroutineBody>" and _input[i + 2][0] == "<statements>":
            vm_writer.write_function(temp_name, 0, function_type, is_void)
            i += 3
        elif _input[i][0] == "</varDec>" and _input[i + 1][0] == "<statements>":
            vm_writer.write_function(temp_name, symbol_table.var_count("var"),
                                     function_type, is_void)
            i += 2
        else:
            i += 1


if "__main__" == __name__:
    # Parses the input path and calls compile_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: JackCompiler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".jack":
            continue
        output_path = filename + ".vm"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            compile_file(input_file, output_file)
