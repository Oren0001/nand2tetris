// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(REFRESH)
    @SCREEN
    D=A
    @screenrow // will store the screen addresses at ascending order
    M=D

    @KBD
    D=M
    @BLACK
    D;JGT // if (KBD > 0) goto BLACK

    @WHITE
    D;JEQ // if (KBD == 0) go to WHITE

    @REFRESH
    0;JMP // else goto REFRESH

(BLACK)
    @blackorwhite
    M=-1
    @FILL
    0;JMP

(WHITE)
    @blackorwhite
    M=0

(FILL)
    // fill a screen row with the correct color
    @blackorwhite
    D=M
    @screenrow
    A=M
    M=D

    // update the screen row + if (screenrow != KBD) goto FILL
    @screenrow
    M=M+1
    D=M
    @KBD
    D=D-A
    @FILL
    D;JNE

    // else goto REFRESH
    @REFRESH
    0;JMP
