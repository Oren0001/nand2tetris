// This file is part of the materials accompanying the book
// "The Elements of Computing Systems" by Nisan and Schocken, 
// MIT Press 2004. Book site: http://www.idc.ac.il/tecs
// File name: projects/04/mult/Mult.tst.   Version: beta 1.4.

load Mult.asm,
output-file MultDrive.out,
compare-to MultDrive.cmp,
output-list RAM[2]%D2.6.2;

set RAM[0] 0,
set RAM[1] 0;
repeat 20 {
  ticktock;
}
output;

set PC 0,
set RAM[0] 1,
set RAM[1] 0;
repeat 50 {
  ticktock;
}
output;

set PC 0,
set RAM[0] 0,
set RAM[1] 2;
repeat 80 {
  ticktock;
}
output;

set PC 0,
set RAM[0] 3,
set RAM[1] 1;
repeat 120 {
  ticktock;
}
output;

set PC 0,
set RAM[0] 2,
set RAM[1] 4;
repeat 150 {
  ticktock;
}
output;

set PC 0,
set RAM[0] 6,
set RAM[1] 7;
repeat 210 {
  ticktock;
}
output;
