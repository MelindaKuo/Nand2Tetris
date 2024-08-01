
class CodeWriter:

    def __init__(self, outFile):
        self.outFile = outFile
        self.file = open(self.outputFile, 'w')

    

    def get_segment_pointer(self, segment, index):
        if segment == "local":
            return f'@LCL\nD=M\n@{index}\nA=D+A'
        if segment == "argument":
            return f'@ARG\nD=M\n@{index}\nA=D+A'
        if segment == "this":
            return f'@THIS\nD=M\n@{index}\nA=D+A'
        if segment == "that":
            return f'@THAT\nD=M\n@{index}\nA=D+A'
        if segment == "static":
            return f'@{self.file}'
        if segment == "temp":
            return f'@R{5+index}'
        if segment == "pointer":
            return f'@R{3+index}'
        

    
    def push_logic(self, segment, index):
        segment_pointer = self.get_segment_pointer(segment, index)
        if segment == "constant":
            return f'@{index}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1'
        else:
            return segment_pointer + '\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1'
    
    def pop_logic(self, segment, index):
        segment_pointer = self.get_segment_pointer(segment, index)
        return f'@SP\nM=M-1\nA=M\nD=M\n{segment_pointer}\nM=D'
    

    def define_Arithmetic(self, operation):
        if operation == "add":
            return "M+D"
        if operation == "sub":
            return "M-D"
        if operation == "neg":
            return "-M"
        if operation == "eq":
            return "JEQ"
        if operation == "gt":
            return "JGT"
        if operation == "lt":
            return "JLT"
        if operation == "and":
            return "M&D"
        if operation == "or":
            return "M|D"
        if operation == "not":
            return "!M"
        

    def writePushPop(self, command,segment, index):
        if command == "C_PUSH":
            self.push_logic(segment, index)
        else:
            self.pop_logic(segment, index)

    def writeArithmetic(self, )




        


        



    



    def close(self):
        self.file.close()
