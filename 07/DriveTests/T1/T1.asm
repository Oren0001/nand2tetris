@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
D=A
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
@TRUE1
D;JEQ
@SP
A=M
M=0
@ENDIF1
0;JMP
(TRUE1)
@SP
A=M
M=-1
(ENDIF1)
@SP
M=M+1
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
@R14
M=D
D=1
M=D&M
@SP
A=M-1
A=A-1
D=M
@R13
M=D
D=1
M=D&M
@SP
M=M-1
A=M
D=M
D=D>>
@SP
M=M-1
A=M
M=M>>
D=M-D
@ISNOTEQ2
D;JNE
@R14
D=M
@R13
D=M-D
(ISNOTEQ2)
@TRUE2
D;JLT
@SP
A=M
M=0
@ENDIF2
0;JMP
(TRUE2)
@SP
A=M
M=-1
(ENDIF2)
@SP
M=M+1
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
@R14
M=D
D=1
M=D&M
@SP
A=M-1
A=A-1
D=M
@R13
M=D
D=1
M=D&M
@SP
M=M-1
A=M
D=M
D=D>>
@SP
M=M-1
A=M
M=M>>
D=M-D
@ISNOTEQ3
D;JNE
@R14
D=M
@R13
D=M-D
(ISNOTEQ3)
@TRUE3
D;JGT
@SP
A=M
M=0
@ENDIF3
0;JMP
(TRUE3)
@SP
A=M
M=-1
(ENDIF3)
@SP
M=M+1
@56
D=A
@SP
A=M
M=D
@SP
M=M+1
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
@53
D=A
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
@112
D=A
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
@SP
M=M-1
A=M
M=-M
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D&M
@SP
A=M
M=D
@SP
M=M+1
@82
D=A
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
D=D|M
@SP
A=M
M=D
@SP
M=M+1
