// key pressed = screen black ; no key pressed= clear screen 
// key must be pressed long enough for the full result to show





(START)

@KBD
D=M
@WHITE
D;JEQ

@color
M=-1
@WHITEEND
0;JMP

(WHITE)
@color
M=0
(WHITEEND)

@SCREEN
D=A
@address
M=D

(LOOP)

@color
D=M
@address
A=M
M=D

@address
M=M+1
D=M

@KBD
D=D-A
@LOOP
D;JNE

@START
0;JMP
