// R2=  R0*R1
// can't modify R0 or R1

// R2+R0
// Loop while R1 >0 
// R2+R0 --> R1-1


@R0
D=M

@R2
M=0


(LOOP)

@R1
D=M

@END
D;JEQ

@value1
M=D

@R0
D=M


@R2
M=D

@value1
M=M-1

@LOOP
0;JMP

@END
0;JMP





