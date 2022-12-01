"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    STATEMENTS = ("while", "if", "let", "do", "return")
    TYPES = ("int", "char", "boolean", "void")
    RULES = ("class", "classVarDec", "subroutineDec", "subroutineBody",
             "parameterList", "varDec", "statements", "doStatement",
             "letStatement", "whileStatement", "returnStatement",
             "ifStatement", "expression", "term", "expressionList")

    def __init__(self, input_, output) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_: A list which contains pairs of token and it's type.
        :param output: The output stream.
        """
        self._input = input_
        self._output = output
        self._cur = 0
        self._methods_names = dict()

    def get_methods_names(self):
        return self._methods_names

    def _write_lines(self, n):
        for i in range(n):
            _token = self._input[self._cur][0]
            _type = self._input[self._cur][1]
            self._output.append([_type, _token])
            self._cur += 1

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self._output.append([f"<{self.RULES[0]}>"])

        self._write_lines(3)
        # field or static
        while self._input[self._cur][0] in JackTokenizer.KEYWORDS[4:6]:
            self.compile_class_var_dec()
        # constructor, function or method
        while self._input[self._cur][0] in JackTokenizer.KEYWORDS[1:4]:
            self.compile_subroutine_dec()
        self._write_lines(1)

        self._output.append([f"</{self.RULES[0]}>"])

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self._output.append([f"<{self.RULES[1]}>"])

        self._write_lines(3)
        # token == ","
        while self._input[self._cur][0] == JackTokenizer.SYMBOLS[7]:
            self._write_lines(2)
        self._write_lines(1)

        self._output.append([f"</{self.RULES[1]}>"])

    def compile_subroutine_dec(self) -> None:
        self._output.append([f"<{self.RULES[2]}>"])

        if self._input[self._cur][0] == JackTokenizer.KEYWORDS[3]:
            self._methods_names[self._input[self._cur + 2][0]] = True
            if self._input[self._cur + 1][0] == JackTokenizer.KEYWORDS[10]:
                self._methods_names[self._input[self._cur + 2][0]] = False
        self._write_lines(4)
        self.compile_parameter_list()
        self._write_lines(1)
        self.compile_subroutine()

        self._output.append([f"</{self.RULES[2]}>"])

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        self._output.append([f"<{self.RULES[3]}>"])

        self._write_lines(1)
        # token == "var"
        while self._input[self._cur][0] == JackTokenizer.KEYWORDS[6]:
            self.compile_var_dec()
        self.compile_statements()
        self._write_lines(1)

        self._output.append([f"</{self.RULES[3]}>"])

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        self._output.append([f"<{self.RULES[4]}>"])

        # token != ")"
        if self._input[self._cur][0] != JackTokenizer.SYMBOLS[3]:
            while True:
                self._write_lines(2)
                # token != ","
                if self._input[self._cur][0] != JackTokenizer.SYMBOLS[7]:
                    break
                else:
                    self._write_lines(1)

        self._output.append([f"</{self.RULES[4]}>"])

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self._output.append([f"<{self.RULES[5]}>"])

        self._write_lines(3)
        while self._input[self._cur][0] == ',':
            self._write_lines(2)
        self._write_lines(1)

        self._output.append([f"</{self.RULES[5]}>"])

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        self._output.append([f"<{self.RULES[6]}>"])

        while True:
            token = self._input[self._cur][0]
            if token == self.STATEMENTS[0]:
                self.compile_while()
            elif token == self.STATEMENTS[1]:
                self.compile_if()
            elif token == self.STATEMENTS[2]:
                self.compile_let()
            elif token == self.STATEMENTS[3]:
                self.compile_do()
            elif token == self.STATEMENTS[4]:
                self.compile_return()
            else:
                break

        self._output.append([f"</{self.RULES[6]}>"])

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self._output.append([f"<{self.RULES[7]}>"])
        temp_output = self._output
        self._output = list()

        self._write_lines(1)
        self.compile_subroutine_call()
        self._write_lines(1)

        temp_output.append(self._output)
        self._output = temp_output
        self._output.append([f"</{self.RULES[7]}>"])

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self._output.append([f"<{self.RULES[8]}>"])
        temp_output = self._output
        self._output = list()

        self._write_lines(2)
        # ['expression'] ?
        if self._input[self._cur][0] == '[':
            self._write_lines(1)
            self.compile_expression()
            self._write_lines(1)
        self._write_lines(1)
        self.compile_expression()
        self._write_lines(1)

        temp_output.append(self._output)
        self._output = temp_output
        self._output.append([f"</{self.RULES[8]}>"])

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self._output.append([f"<{self.RULES[9]}>"])
        temp_output = self._output
        self._output = list()

        self._write_lines(2)
        self.compile_expression()
        self._write_lines(2)
        self.compile_statements()
        self._write_lines(1)

        temp_output.append(self._output)
        self._output = temp_output
        self._output.append([f"</{self.RULES[9]}>"])

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self._output.append([f"<{self.RULES[10]}>"])
        temp_output = self._output
        self._output = list()

        self._write_lines(1)
        # token != ";"
        if self._input[self._cur][0] != JackTokenizer.SYMBOLS[8]:
            self.compile_expression()
        self._write_lines(1)

        temp_output.append(self._output)
        self._output = temp_output
        self._output.append([f"</{self.RULES[10]}>"])

    def compile_else(self) -> None:
        self._write_lines(2)
        self.compile_statements()
        self._write_lines(1)

    def compile_if(self) -> None:
        """Compiles an if statement, possibly with a trailing else clause."""
        self._output.append([f"<{self.RULES[11]}>"])
        temp_output = self._output
        self._output = list()

        self._write_lines(2)
        self.compile_expression()
        self._write_lines(2)
        self.compile_statements()
        self._write_lines(1)
        # token == "else"
        if self._input[self._cur][0] == JackTokenizer.KEYWORDS[18]:
            self.compile_else()

        temp_output.append(self._output)
        self._output = temp_output
        self._output.append([f"</{self.RULES[11]}>"])

    def compile_subroutine_call(self) -> None:
        self._write_lines(1)
        if self._input[self._cur][0] == '.':
            self._write_lines(2)
        self._write_lines(1)
        self.compile_expression_list()
        self._write_lines(1)

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self._output.append([f"<{self.RULES[12]}>"])
        temp_output = self._output
        self._output = list()

        while True:
            self.compile_term()
            # token in ["+", "=", "*", "/", "&", "|", "<", ">", "-"]
            if self._input[self._cur][0] in JackTokenizer.SYMBOLS[9:18]:
                self._write_lines(1)
            else:
                break

        temp_output.append(self._output)
        self._output = temp_output
        self._output.append([f"</{self.RULES[12]}>"])

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "."
        suffices to distinguish between the three possibilities. Any other
        token is not part of this term and should not be advanced over.
        """
        # token == "("
        if self._input[self._cur][0] == JackTokenizer.SYMBOLS[2]:
            self._write_lines(1)
            self.compile_expression()
            self._write_lines(1)
        # second token == unary operator
        elif self._input[self._cur][0] in JackTokenizer.SYMBOLS[-4:]:
            self._write_lines(1)
            self.compile_term()
        # second token == "(" or second token == "."
        elif self._input[self._cur + 1][0] == JackTokenizer.SYMBOLS[6] or \
                self._input[self._cur + 1][0] == JackTokenizer.SYMBOLS[2]:
            self.compile_subroutine_call()
        # second token == "["
        elif self._input[self._cur + 1][0] == JackTokenizer.SYMBOLS[4]:
            self._write_lines(2)
            self.compile_expression()
            self._write_lines(1)
        else:
            self._write_lines(1)

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self._output.append([f"<{self.RULES[14]}>"])

        # token != ")"
        if self._input[self._cur][0] != JackTokenizer.SYMBOLS[3]:
            while True:
                self.compile_expression()
                # token != ","
                if self._input[self._cur][0] != JackTokenizer.SYMBOLS[7]:
                    break
                else:
                    self._write_lines(1)

        self._output.append([f"</{self.RULES[14]}>"])
