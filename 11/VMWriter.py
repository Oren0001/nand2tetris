"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class VMWriter:
    """
    Writes VM commands into a file. Encapsulates the VM command syntax.
    """

    OPERATORS = ('+', '*', '/', '&', '|', '<', '>', '=', '-')
    UNARY_OPERATORS = ('-', '~', '^', '#')
    OS_VOID_METHODS = ("init", "dispose", "setCharAt", "eraseLastChar", "setInt",
                       "poke", "deAlloc")
    OS_VOID_CLASSES = ("Output", "Screen", "Sys")
    OS_CLASSES = ("Math", "String", "Array", "Output", "Screen", "Keyboard",
                  "Memory", "Sys")

    def __init__(self, output_stream: typing.TextIO, symbol_table,
                 methods_names) -> None:
        """Creates a new file and prepares it for writing VM commands."""
        self._output = output_stream
        self._label_count = 0
        self._symbol_table = symbol_table
        self._is_void = bool()
        self._methods_names = methods_names
        self._do_method = [None, None]

    def write_push(self, var, segment=None, index=None) -> None:
        """Writes a VM push command.

        Args:
            var: A variable.
            index (int): the index to push to.
            segment (str): the segment to push to, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP"
        """
        if var is None:
            self._output.write(f"push {segment} {index}\n")
            return
        kind = self._symbol_table.kind_of(var)
        if kind is not None:
            index = self._symbol_table.index_of(var)
            self._output.write(f"push {kind} {index}\n")
        elif var == "this":
            self._output.write("push pointer 0\n")
        elif var == "that":
            self._output.write("push pointer 1\n")
        elif var.isdecimal():
            self._output.write(f"push constant {var}\n")
        elif var == "true":
            self._output.write("push constant 0\n")
            self._output.write("not\n")
        elif var == "false":
            self._output.write("push constant 0\n")
        elif var == "null":
            self._output.write("push constant 0\n")
        elif var[0] == '"':
            n = len(var) - 2
            self._output.write(f"push constant {n}\n")
            self._output.write("call String.new 1\n")
            for char in var[1:-1]:
                unicode_value = ord(char)
                self._output.write(f"push constant {unicode_value}\n")
                self._output.write("call String.appendChar 2\n")

    def write_pop(self, var, segment=None, index=None) -> None:
        """Writes a VM pop command.

        Args:
            var: A variable.
            segment (str): the segment to pop from, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP".
            index (int): the index to pop from.
        """
        if var is not None:
            kind = self._symbol_table.kind_of(var)
            i = self._symbol_table.index_of(var)
            self._output.write(f"pop {kind} {i}\n")
        else:
            self._output.write(f"pop {segment} {index}\n")

    def write_arithmetic(self, command: str) -> None:
        """Writes a VM arithmetic command.

        Args:
            command (str): the command to write, can be "ADD", "SUB", "NEG", 
            "EQ", "GT", "LT", "AND", "OR", "NOT".
        """
        if command == '+':
            self._output.write("add\n")
        elif command == '-':
            self._output.write("sub\n")
        elif command == '*':
            self._output.write("call Math.multiply 2\n")
        elif command == '/':
            self._output.write("call Math.divide 2\n")
        elif command == '&':
            self._output.write("and\n")
        elif command == '|':
            self._output.write("or\n")
        elif command == '=':
            self._output.write("eq\n")
        elif command == '>':
            self._output.write("gt\n")
        elif command == '<':
            self._output.write("lt\n")
        elif command == "neg":
            self._output.write("neg\n")
        elif command == '~':
            self._output.write("not\n")
        elif command == '^':
            self._output.write("shiftleft\n")
        elif command == '#':
            self._output.write("shiftright\n")

    def write_label(self, label: int) -> None:
        """Writes a VM label command.

        Args:
            label (str): the label to write.
        """
        self._output.write(f"label {label}\n")

    def write_goto(self, label: int) -> None:
        """Writes a VM goto command.

        Args:
            label (str): the label to go to.
        """
        self._output.write(f"goto {label}\n")

    def write_if(self, label: int) -> None:
        """Writes a VM if-goto command.

        Args:
            label (str): the label to go to.
        """
        self._output.write(f"if-goto {label}\n")

    def write_call(self, name: str, n_args: int) -> None:
        """Writes a VM call command.

        Args:
            name (str): the name of the function to call.
            n_args (int): the number of arguments the function receives.
        """
        self._output.write(f"call {name} {n_args}\n")

    def write_function(self, name: str, n_locals: int, function_type, is_void) -> None:
        """Writes a VM function command.

        Args:
            name (str): the name of the function.
            n_locals (int): the number of local variables the function uses.
            function_type: "function", "method" or "constructor"
            is_void: True if the function returns void, otherwise False.
        """
        self._is_void = is_void
        name = self._symbol_table.get_class_name() + '.' + name
        self._output.write(f"function {name} {n_locals}\n")
        if function_type == "method":
            self.write_push(None, "argument", 0)
            self.write_pop(None, "pointer", 0)
        elif function_type == "constructor":
            self.write_constructor()

    def write_return(self) -> None:
        """Writes a VM return command."""
        self._output.write("return\n")

    def write_expression(self, exp):
        if len(exp) == 0:
            return
        if len(exp) == 1:
            self.write_push(exp[0])
            return
        if exp[0] in self.UNARY_OPERATORS:
            self.write_expression(exp[1:])
            if exp[0] == '-':
                self.write_arithmetic("neg")
            else:
                self.write_arithmetic(exp[0])
            return
        i = -1
        for op in self.OPERATORS:
            try:
                i = exp.index(op)
                break
            except ValueError:
                continue
        if i != -1:
            self.write_expression(exp[:i])
            self.write_expression(exp[i + 1:])
            self.write_arithmetic(exp[i])
        elif exp[0] == '(':
            self.write_expression(exp[1])
        elif exp[1] == '(' and exp[0] not in self.UNARY_OPERATORS:
            k = 0
            if self._methods_names.get(exp[0]) is not None:
                k = 1
                self.write_push(None, "pointer", 0)
            i = exp.index(')')
            arguments = exp[2:i]
            for e in arguments:
                self.write_expression(e)
            self.write_call(self._symbol_table.get_class_name() + '.' + exp[0],
                            len(arguments) + k)
            if self._methods_names.get(exp[0]) is False:
                self.write_pop(None, "temp", 0)
        elif exp[1] == '.' and exp[3] == '(':
            k = 0
            if self._symbol_table.kind_of(exp[0]):
                k = 1
                self.write_push(exp[0])
            i = exp.index(')')
            arguments = exp[4:i]
            for e in arguments:
                self.write_expression(e)
            _type = self._symbol_table.type_of(exp[0])
            if _type is None:
                _type = exp[0]
            self.write_call(_type + '.' + exp[2], len(arguments) + k)
            if self._methods_names.get(exp[0]) is False or \
                    exp[0] in self.OS_VOID_CLASSES or exp[2] in self.OS_VOID_METHODS or \
                    (exp[0] == self._do_method[0] and exp[2] == self._do_method[1]):
                self.write_pop(None, "temp", 0)
        elif exp[1] == '[':
            self.write_push(exp[0])
            self.write_expression(exp[2])
            self.write_arithmetic('+')
            self.write_pop(None, "pointer", 1)
            self.write_push(None, "that", 0)

    def get_expression(self, exp):
        res = list()
        i = 0
        while i < len(exp):
            if exp[i][0] == "<expression>":
                res.append(self.get_expression(exp[i + 1]))
                i += 3
            elif len(exp[i]) == 1:
                i += 1
            elif len(exp[i]) == 2 and exp[i][1] != ',':
                res.append(exp[i][1])
                i += 1
            else:
                i += 1
        return res

    def write_statements(self, statement, _input):
        if statement == "<ifStatement>":
            i = 0
            flag = 1
            temp = self._label_count
            self._label_count += 2
            while i < len(_input):
                if _input[i][0] == "<expression>":
                    exp = self.get_expression(_input[i + 1])
                    i += 3
                    self.write_expression(exp)
                    self.write_arithmetic("~")
                    self.write_if(temp)
                elif type(_input[i][0]) == str and _input[i][0].endswith("Statement>"):
                    self.write_statements(_input[i][0], _input[i + 1])
                    i += 3
                elif _input[i][0] == "</statements>" and flag == 1:
                    flag = 0
                    self.write_goto(temp + 1)
                    self.write_label(temp)
                    i += 1
                else:
                    i += 1
            self.write_label(temp + 1)
        elif statement == "<whileStatement>":
            i = 0
            temp = self._label_count
            self._label_count += 2
            self.write_label(temp)
            while i < len(_input):
                if _input[i][0] == "<expression>":
                    exp = self.get_expression(_input[i + 1])
                    i += 3
                    self.write_expression(exp)
                    self.write_arithmetic("~")
                    self.write_if(temp + 1)
                elif type(_input[i][0]) == str and _input[i][0].endswith("Statement>"):
                    self.write_statements(_input[i][0], _input[i + 1])
                    i += 3
                elif _input[i][0] == "</statements>":
                    i += 1
                    self.write_goto(temp)
                else:
                    i += 1
            self.write_label(temp + 1)
        elif statement == "<letStatement>":
            if _input[2][1] == '[':
                # push arr
                self.write_push(_input[1][1])
                # expression 1
                exp = self.get_expression(_input[4])
                self.write_expression(exp)
                # add
                self.write_arithmetic('+')
                # expression 2
                exp = self.get_expression(_input[9])
                self.write_expression(exp)
                # temp 0 = value of expression 2
                self.write_pop(None, "temp", 0)

                self.write_pop(None, "pointer", 1)
                self.write_push(None, "temp", 0)
                self.write_pop(None, "that", 0)
            else:
                var = _input[1][1]
                exp = self.get_expression(_input[4])
                self.write_expression(exp)
                self.write_pop(var)
        elif statement == "<doStatement>":
            if len(_input) >= 4 and type(_input[1]) == list and type(_input[3]) == list \
                    and len(_input[1]) == 2 and len(_input[3]) == 2:
                self._do_method = [_input[1][1], _input[3][1]]
            exp = self.get_expression(_input[1:])
            self.write_expression(exp)
        elif statement == "<returnStatement>":
            if len(_input) > 2:
                exp = self.get_expression(_input[2])
                self.write_expression(exp)
            if self._is_void:
                self.write_push(str(0))
            self.write_return()

    def write_constructor(self):
        n = self._symbol_table.var_count("field")
        self.write_push(str(n))
        self._output.write(f"call Memory.alloc 1\n")
        self.write_pop(None, "pointer", 0)
