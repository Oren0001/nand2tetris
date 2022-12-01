"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    VM_SEGMENTS = ("local", "argument", "this", "that", "temp", "pointer",
                   "constant", "static")
    TEMP_START_ADDRESS = '5'
    POINTER_START_ADDRESS = '3'
    ASM_SEGMENTS = {"local": "LCL", "argument": "ARG", "this": "THIS",
                    "that": "THAT", "temp": TEMP_START_ADDRESS,
                    "pointer": POINTER_START_ADDRESS}
    COMMANDS = ("push", "pop")
    STACK_POINTER = "SP"
    VM_OPERATIONS = ("sub", "add", "and", "or", "eq", "gt", "lt", "neg",
                     "not", "shiftleft", "shiftright")
    ASM_OPERATIONS = {"sub": '-', "add": '+', "and": '&', "or": '|',
                      "eq": "JEQ", "gt": "JGT", "lt": "JLT"}
    SAVED_ADDRESSES_NUM = '5'

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self._output = output_stream
        self._filename = str()
        self._label_num = 1

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        self._filename = filename

    def stack_pop(self):
        """
        Removes the last item from the stack, and stores it at register D.
        """
        self._output.write(f"@{self.STACK_POINTER}\n")
        self._output.write("M=M-1\n")
        self._output.write("A=M\n")
        self._output.write("D=M\n")

    def stack_push(self):
        """
        Puts register D's value in the address that is pointed by sp.
        """
        self._output.write(f"@{self.STACK_POINTER}\n")
        self._output.write("A=M\n")
        self._output.write("M=D\n")

    def increment_sp(self):
        """
        Increments the stack pointer by 1.
        """
        self._output.write(f"@{self.STACK_POINTER}\n")
        self._output.write("M=M+1\n")

    def _not(self):
        # D = stack.pop
        self.stack_pop()
        # D = not D
        self._output.write("D=!D\n")
        # *SP = D
        self.stack_push()
        # SP++
        self.increment_sp()

    def neg(self):
        # change to negative value
        self._output.write(f"@{self.STACK_POINTER}\n")
        self._output.write("M=M-1\n")
        self._output.write("A=M\n")
        self._output.write("M=-M\n")
        # SP++
        self.increment_sp()

    def eq_gt_lt(self, command):
        asm_condition = self.ASM_OPERATIONS[command]
        if command == self.VM_OPERATIONS[4]:
            self.stack_pop()
            self._output.write(f"@{self.STACK_POINTER}\n")
            self._output.write("M=M-1\n")
            self._output.write("A=M\n")
            self._output.write("D=M-D\n")
        # handle overflow
        else:
            # put first bit of addend2 in R14
            self._output.write(f"@{self.STACK_POINTER}\n")
            self._output.write("A=M-1\n")
            self._output.write("D=M\n")
            self._output.write("@R14\n")
            self._output.write("M=D\n")
            self._output.write("D=1\n")
            self._output.write("M=D&M\n")
            # put first bit of addend1 in R13
            self._output.write(f"@{self.STACK_POINTER}\n")
            self._output.write("A=M-1\n")
            self._output.write("A=A-1\n")
            self._output.write("D=M\n")
            self._output.write("@R13\n")
            self._output.write("M=D\n")
            self._output.write("D=1\n")
            self._output.write("M=D&M\n")
            # D = (addend1 / 2) - (addend2 / 2)
            self.stack_pop()
            self._output.write("D=D>>\n")
            self._output.write(f"@{self.STACK_POINTER}\n")
            self._output.write("M=M-1\n")
            self._output.write("A=M\n")
            self._output.write("M=M>>\n")
            self._output.write("D=M-D\n")
            # if (D != 0) goto (ISNOTEQ) else D=R13-R14
            self._output.write(f"@ISNOTEQ{self._label_num}\n")
            self._output.write("D;JNE\n")
            self._output.write("@R14\n")
            self._output.write("D=M\n")
            self._output.write("@R13\n")
            self._output.write("D=M-D\n")
            self._output.write(f"(ISNOTEQ{self._label_num})\n")
        # if (D == 0) or (D > 0) or (D < 0) goto (TRUE)
        self._output.write(f"@TRUE{self._label_num}\n")
        self._output.write(f"D;{asm_condition}\n")
        self._output.write(f"@{self.STACK_POINTER}\n")
        self._output.write("A=M\n")
        self._output.write("M=0\n")
        self._output.write(f"@ENDIF{self._label_num}\n")
        self._output.write("0;JMP\n")
        # (TRUE)
        self._output.write(f"(TRUE{self._label_num})\n")
        self._output.write(f"@{self.STACK_POINTER}\n")
        self._output.write("A=M\n")
        self._output.write("M=-1\n")
        self._output.write(f"(ENDIF{self._label_num})\n")
        # SP++
        self.increment_sp()

        self._label_num += 1

    def sub_add_and_or(self, command):
        asm_operation = self.ASM_OPERATIONS[command]
        if command == self.VM_OPERATIONS[0]:
            result = f"M{asm_operation}D"
        else:
            result = f"D{asm_operation}M"
        # D = operation between left hand side and right hand side
        self.stack_pop()
        self._output.write(f"@{self.STACK_POINTER}\n")
        self._output.write("M=M-1\n")
        self._output.write("A=M\n")
        self._output.write(f"D={result}\n")
        # *SP = D
        self.stack_push()
        # SP++
        self.increment_sp()

    def write_arithmetic(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given 
        arithmetic command.

        Args:
            command (str): an arithmetic command.
        """
        if command in self.VM_OPERATIONS[0:4]:
            self.sub_add_and_or(command)
        elif command in self.VM_OPERATIONS[4:7]:
            self.eq_gt_lt(command)
        elif command == self.VM_OPERATIONS[7]:
            self.neg()
        elif command == self.VM_OPERATIONS[8]:
            self._not()

    def pop_static(self, i):
        # D = stack.pop
        self.stack_pop()
        # update the static variable's value
        self._output.write(f"@{self._filename}.{i}\n")
        self._output.write("M=D\n")

    def push_static(self, i):
        # put the static variable's value in D
        self._output.write(f"@{self._filename}.{i}\n")
        self._output.write("D=M\n")
        # *SP = D
        self.stack_push()
        # SP++
        self.increment_sp()

    def write_static(self, command, i):
        if command == self.COMMANDS[0]:
            self.push_static(i)
        elif command == self.COMMANDS[1]:
            self.pop_static(i)

    def push_constant(self, i):
        # *SP = i
        self._output.write(f"@{i}\n")
        self._output.write("D=A\n")
        self.stack_push()
        # SP++
        self.increment_sp()

    def pop_local_argument_this_that_temp_pointer(self, asm_segment, i):
        # addr = segmentPointer+i
        self._output.write(f"@{asm_segment}\n")
        if asm_segment == self.TEMP_START_ADDRESS or \
                asm_segment == self.POINTER_START_ADDRESS:
            command = "D=A\n"
        else:
            command = "D=M\n"
        self._output.write(command)
        self._output.write(f"@{i}\n")
        self._output.write("D=D+A\n")
        self._output.write("@R13\n")
        self._output.write("M=D\n")
        # D = stack.pop
        self.stack_pop()
        # *addr = *SP
        self._output.write("@R13\n")
        self._output.write("A=M\n")
        self._output.write("M=D\n")

    def push_local_argument_this_that_temp_pointer(self, asm_segment, i):
        # addr = segmentPointer+i
        self._output.write(f"@{asm_segment}\n")
        if asm_segment == self.TEMP_START_ADDRESS or \
                asm_segment == self.POINTER_START_ADDRESS:
            command = "D=A\n"
        else:
            command = "D=M\n"
        self._output.write(command)
        self._output.write(f"@{i}\n")
        self._output.write("D=D+A\n")
        self._output.write("A=D\n")
        self._output.write("D=M\n")
        # *SP = *addr
        self.stack_push()
        # SP++
        self.increment_sp()

    def write_local_argument_this_that_temp_pointer(self, command, segment, i):
        asm_segment = self.ASM_SEGMENTS[segment]
        if command == self.COMMANDS[0]:
            self.push_local_argument_this_that_temp_pointer(asm_segment, i)
        elif command == self.COMMANDS[1]:
            self.pop_local_argument_this_that_temp_pointer(asm_segment, i)

    def write_push_pop(self, command: str, segment: str, index: str) -> None:
        """Writes the assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (str): the index in the memory segment.
        """
        if segment in self.VM_SEGMENTS[:6]:
            self.write_local_argument_this_that_temp_pointer(command, segment,
                                                             index)
        elif segment == self.VM_SEGMENTS[6]:
            self.push_constant(index)
        elif segment == self.VM_SEGMENTS[7]:
            self.write_static(command, index)

    def write_shift(self, command: str) -> None:
        self.stack_pop()
        if command == self.VM_OPERATIONS[9]:
            self._output.write("D=D<<\n")
        else:
            self._output.write("D=D>>\n")
        self.stack_push()
        self.increment_sp()
