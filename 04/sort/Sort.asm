// This file is part of nand2tetris, as taught in The Hebrew University,
// and was written by Aviv Yaish, and is published under the Creative 
// Common Attribution-NonCommercial-ShareAlike 3.0 Unported License 
// https://creativecommons.org/licenses/by-nc-sa/3.0/

// An implementation of a sorting algorithm. 
// An array is given in R14 and R15, where R14 contains the start address of the 
// array, and R15 contains the length of the array. 
// You are not allowed to change R14, R15.
// The program should sort the array in-place and in descending order - 
// the largest number at the head of the array.
// You can assume that each array value x is between -16384 < x < 16384.
// You can assume that the address in R14 is at least >= 2048, and that 
// R14 + R15 <= 16383. 
// No other assumptions can be made about the length of the array.
// You can implement any sorting algorithm as long as its runtime complexity is 
// at most C*O(N^2), like bubble-sort. 

// Put your code here.

// bubble sort:
    @R15

    D=M-1
    D=D-1
    @END
    D;JLT
    @stop // stop = R15-2
    M=D

    @i
    M=0

(OUTERLOOP)
    // if (i <= stop) goto DO1, else goto END
    @i
    D=M
    @stop
    D=D-M
    @DO1
    D;JLE
    @END
    0;JMP

    (DO1)
        @swapped
        M=0

        @j
        M=0

        (INNERLOOP)
            // if (j <= stop-i) goto DO2, else goto CHECKSWAPPED
            @stop
            D=M
            @i
            D=D-M
            @j
            D=M-D
            @DO2
            D;JLE
            @CHECKSWAPPED
            0;JMP

            (DO2)
                // if (arr[j] < arr[j+1]) goto SWAP, else goto INCREASEJ
                @R14
                D=M
                @j
                D=D+M
                @pointer0
                M=D
                D=M+1
                @pointer1
                M=D

                A=D
                D=M
                @pointer0
                A=M
                D=M-D
                @SWAP
                D;JLT
                @INCREASEJ
                0;JMP

                (SWAP)
                    // save arr[j+1] in variable temp
                    @pointer1
                    A=M
                    D=M
                    @temp
                    M=D

                    // store arr[j] in arr[j+1]
                    @pointer0
                    A=M
                    D=M
                    @pointer1
                    A=M
                    M=D

                    // store temp in arr[j]
                    @temp
                    D=M
                    @pointer0
                    A=M
                    M=D

                    @swapped
                    M=1

                (INCREASEJ)
                    @j
                    M=M+1
                    @INNERLOOP
                    0;JMP

        (CHECKSWAPPED)
            // if (swapped == 0) goto END
            @swapped
            D=M
            @END
            D;JEQ

            // else i++; if (i <= stop) goto OUTERLOOP
            @i
            M=M+1
            D=M
            @stop
            D=D-M
            @OUTERLOOP
            D;JLE

    (END)
        @END
        0;JMP
