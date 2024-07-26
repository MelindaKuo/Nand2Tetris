// R2=  R0*R1
// can't modify R0 or R1

@R0
D=M       
@R2
M=0      

@R1
D=M      // make copy of R1
@R3
M=D      

(LOOP)
@R3
D=M       
@END
D;JEQ         // if R1 is <0 exit

@R0
D=M       // add R0 and R2 together
@R2
M=D+M    

@R3
M=M-1     // decrease 1 from R2
@LOOP
0;JMP         // continue the loop    

(END)
@END
0;JMP     

