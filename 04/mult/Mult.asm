// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

    @R2
    M=0

// implement greater = max(R0,R1); lower = min(R0,R1)
    @R1
    D=M
    @R0
    D=D-M
    @LABEL1
    D;JGE

    @R0
    D=M
    @greater
    M=D

    @R1
    D=M
    @lower
    M=D

    @LOOP
    0;JMP

(LABEL1)
    @R1
    D=M
    @greater
    M=D

    @R0
    D=M
    @lower
    M=D

// implement multiplication
(LOOP)
    @lower
    M=M-1
    D=M
    @END
    D;JLT

    @greater
    D=M
    @R2
    M=D+M

    @LOOP
    0;JMP

(END)
    @END
    0;JMP
