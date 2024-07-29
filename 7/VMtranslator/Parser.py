import os

class Parser:

    command_Arithmetic = {'add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and' 'or', 'not'}
    commands_C= {'push', 'pop', 'label', 'goto', 'if', 'function', 'return',  'call'}

    def __init__(self, input_file):
        self.input_file = input_file
        self.commands = []
        file_open = open(input_file, 'r')
        for line in file_open:
            if line.startswith('//') or line.startswith(" "):
                continue
            else:
                self.commands.append(line.strip())
        self.currInstruction = -1
        self.currCommand = None
        

    def has_more_lines(self):
        return self.currInstruction < len(self.commands)-1
    

    def advance(self):
        self.currInstruction+=1
        self.currCommand = self.commands[self.currInstruction]


    def command_type(self):
        if self.currCommand[0] in self.command_Arithmetic:
            return 'C_ARITHMETIC'
        else:
            for c in self.commands_C:
                if c == self.currCommand[0]:
                    return "C_" + c.upper()
    
    def arg1(self):
        if self.currCommand == "C_ARITHMETIC":
            return self.currCommand[1:]
        else:
            return self.currCommand.split()[1]


    def arg2(self):
        if self.command_type[2:] not in {'PUSH', 'POP', 'FUNCTION', 'CALL'}:
            return self.currCommand.split()[2]
        else:
            raise TypeError("Must be Push/Pop/Function/Call")
    









