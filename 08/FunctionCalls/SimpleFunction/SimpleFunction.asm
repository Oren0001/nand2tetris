@SP
M=0
@256
D=A
@SP
M=D
D=0
@SP
A=M
M=D
@SP
M=M+1
D=0
@SP
A=M
M=D
@SP
M=M+1
D=0
@SP
A=M
M=D
@SP
M=M+1
D=0
@SP
A=M
M=D
@SP
M=M+1
D=0
@SP
A=M
M=D
@SP
M=M+1
@Sys.init
0;JMP
(SimpleFunction.test)
@2
D=A
(LOOP_SIMPLEFUNCTION_1)
@ENDFUNCTION_SIMPLEFUNCTION_1
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
D=D-1
@LOOP_SIMPLEFUNCTION_1
0;JMP
(ENDFUNCTION_SIMPLEFUNCTION_1)
@LCL
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@1
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D+M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
D=!D
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D+M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@1
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@R13
M=D
@5
D=D-A
A=D
D=M
@R14
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
AM=M-1
D=M
@THAT
M=D
@R13
AM=M-1
D=M
@THIS
M=D
@R13
AM=M-1
D=M
@ARG
M=D
@R13
AM=M-1
D=M
@LCL
M=D
@R14
A=M
0;JMP
