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
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@16
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
@TRUE2
D;JEQ
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
@16
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
@TRUE3
D;JEQ
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
@ISNOTEQ4
D;JNE
@R14
D=M
@R13
D=M-D
(ISNOTEQ4)
@TRUE4
D;JLT
@SP
A=M
M=0
@ENDIF4
0;JMP
(TRUE4)
@SP
A=M
M=-1
(ENDIF4)
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@892
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
@ISNOTEQ5
D;JNE
@R14
D=M
@R13
D=M-D
(ISNOTEQ5)
@TRUE5
D;JLT
@SP
A=M
M=0
@ENDIF5
0;JMP
(TRUE5)
@SP
A=M
M=-1
(ENDIF5)
@SP
M=M+1
@891
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
@ISNOTEQ6
D;JNE
@R14
D=M
@R13
D=M-D
(ISNOTEQ6)
@TRUE6
D;JLT
@SP
A=M
M=0
@ENDIF6
0;JMP
(TRUE6)
@SP
A=M
M=-1
(ENDIF6)
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
@ISNOTEQ7
D;JNE
@R14
D=M
@R13
D=M-D
(ISNOTEQ7)
@TRUE7
D;JGT
@SP
A=M
M=0
@ENDIF7
0;JMP
(TRUE7)
@SP
A=M
M=-1
(ENDIF7)
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32767
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
@ISNOTEQ8
D;JNE
@R14
D=M
@R13
D=M-D
(ISNOTEQ8)
@TRUE8
D;JGT
@SP
A=M
M=0
@ENDIF8
0;JMP
(TRUE8)
@SP
A=M
M=-1
(ENDIF8)
@SP
M=M+1
@32766
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
@ISNOTEQ9
D;JNE
@R14
D=M
@R13
D=M-D
(ISNOTEQ9)
@TRUE9
D;JGT
@SP
A=M
M=0
@ENDIF9
0;JMP
(TRUE9)
@SP
A=M
M=-1
(ENDIF9)
@SP
M=M+1
@57
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