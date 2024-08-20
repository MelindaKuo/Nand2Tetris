class CodeWriter:
    def __init__(self, output_file):
        self.output_file = open(output_file, 'w')
        self.file_name = None
        self.label_counter = 0

    def set_file_name(self, file_name):
        self.file_name = file_name

    def write_arithmetic(self, command):
        if command == 'add':
            self._write_binary_operation('M+D')
        elif command == 'sub':
            self._write_binary_operation('M-D')
        elif command == 'neg':
            self._write_unary_operation('-M')
        elif command == 'eq':
            self._write_comparison('JEQ')
        elif command == 'gt':
            self._write_comparison('JGT')
        elif command == 'lt':
            self._write_comparison('JLT')
        elif command == 'and':
            self._write_binary_operation('M&D')
        elif command == 'or':
            self._write_binary_operation('M|D')
        elif command == 'not':
            self._write_unary_operation('!M')

    def write_push_pop(self, command, segment, index):
        if command == 'push':
            if segment == 'constant':
                self._write_push_constant(index)
            else:
                self._write_push_segment(segment, index)
        elif command == 'pop':
            self._write_pop_segment(segment, index)

    def _write_push_constant(self, value):
        self._write_code([
            f'@{value}',
            'D=A',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1'
        ])

    def _write_push_segment(self, segment, index):
        if segment == 'static':
            segment_pointer = f'@{self.file_name}.{index}'
        else:
            segment_pointer = self._get_segment_pointer(segment, index)

        if segment == 'constant':
            self._write_code([
                segment_pointer,
                'D=A',
                '@SP',
                'A=M',
                'M=D',
                '@SP',
                'M=M+1'
            ])
        else:
            self._write_code([
                segment_pointer,
                'D=M',
                '@SP',
                'A=M',
                'M=D',
                '@SP',
                'M=M+1'
            ])

    def _write_pop_segment(self, segment, index):
        if segment == 'static':
            segment_pointer = f'@{self.file_name}.{index}'
        else:
            segment_pointer = self._get_segment_pointer(segment, index)

        self._write_code([
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            segment_pointer,
            'M=D'
        ])

    def _get_segment_pointer(self, segment, index):
        if segment == 'local':
            return f'@LCL\nD=M\n@{index}\nA=D+A'
        elif segment == 'argument':
            return f'@ARG\nD=M\n@{index}\nA=D+A'
        elif segment == 'this':
            return f'@THIS\nD=M\n@{index}\nA=D+A'
        elif segment == 'that':
            return f'@THAT\nD=M\n@{index}\nA=D+A'
        elif segment == 'temp':
            return f'@R{5 + index}'
        elif segment == 'pointer':
            return f'@R{3 + index}'
        else:
            raise ValueError(f'Unknown segment: {segment}')

    def _write_binary_operation(self, operation):
        self._write_code([
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@SP',
            'M=M-1',
            'A=M',
            f'M=M{operation}',
            '@SP',
            'M=M+1'
        ])

    def _write_unary_operation(self, operation):
        self._write_code([
            '@SP',
            'M=M-1',
            'A=M',
            f'M={operation}',
            '@SP',
            'M=M+1'
        ])

    def _write_comparison(self, jump):
        self.label_counter += 1
        label_true = f'TRUE_{self.label_counter}'
        label_end = f'END_{self.label_counter}'
        self._write_code([
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@SP',
            'M=M-1',
            'A=M',
            'D=M-D',
            f'@{label_true}',
            f'D;{jump}',
            '@SP',
            'A=M',
            'M=0',
            f'@{label_end}',
            '0;JMP',
            f'({label_true})',
            '@SP',
            'A=M',
            'M=-1',
            f'({label_end})',
            '@SP',
            'M=M+1'
        ])

    def writeLabel(self,label):
        self._write_code([f'({label})'])

    def writeGoto(self, label):
        self._write_code([
            f'@{label}', 
            '0;JMP'
        ])

    def writeIf(self, label):
        self._write_code([
            '@SP', 
            'M = M-1', 
            'A=M', 
            'D=M', 
            f'@{label}',
            'D;JNE'
        ])
    
    def writeFunction(self, functionName, nVars):
        self._write_code([f'({functionName})'])
        for i in range(nVars):
            self.write_push_pop('push', 'constant', 0)
    
    def writeCall(self, functionName, nArgs):
    return_address = f'{functionName}$ret.{self.label_counter}'
    self.label_counter += 1

    self._write_code([
        # Push return address
        f'@{return_address}',
        'D=A',
        '@SP',
        'A=M',
        'M=D',
        '@SP',
        'M=M+1',

        # Push LCL
        '@LCL',
        'D=M',
        '@SP',
        'A=M',
        'M=D',
        '@SP',
        'M=M+1',

        # Push ARG
        '@ARG',
        'D=M',
        '@SP',
        'A=M',
        'M=D',
        '@SP',
        'M=M+1',

        # Push THIS
        '@THIS',
        'D=M',
        '@SP',
        'A=M',
        'M=D',
        '@SP',
        'M=M+1',

        # Push THAT
        '@THAT',
        'D=M',
        '@SP',
        'A=M',
        'M=D',
        '@SP',
        'M=M+1',

        # ARG = SP - nArgs - 5
        '@SP',
        'D=M',
        f'@{nArgs + 5}',
        'D=D-A',
        '@ARG',
        'M=D',

        # LCL = SP
        '@SP',
        'D=M',
        '@LCL',
        'M=D',

        # Goto function
        f'@{functionName}',
        '0;JMP',

        # Declare return label
        f'({return_address})'
    ])

    
    def writeReturn(self):
    self._write_code([
        # FRAME = LCL (save LCL in a temporary variable)
        '@LCL',
        'D=M',
        '@R13',
        'M=D',

        # RET = *(FRAME - 5) (save return address in a temporary variable)
        '@5',
        'A=D-A',
        'D=M',
        '@R14',
        'M=D',

        # *ARG = pop() (reposition the return value for the caller)
        '@SP',
        'M=M-1',
        'A=M',
        'D=M',
        '@ARG',
        'A=M',
        'M=D',

        # SP = ARG + 1 (restore SP of the caller)
        '@ARG',
        'D=M+1',
        '@SP',
        'M=D',

        # THAT = *(FRAME - 1) (restore THAT)
        '@R13',
        'AM=M-1',
        'D=M',
        '@THAT',
        'M=D',

        # THIS = *(FRAME - 2) (restore THIS)
        '@R13',
        'AM=M-1',
        'D=M',
        '@THIS',
        'M=D',

        # ARG = *(FRAME - 3) (restore ARG)
        '@R13',
        'AM=M-1',
        'D=M',
        '@ARG',
        'M=D',

        # LCL = *(FRAME - 4) (restore LCL)
        '@R13',
        'AM=M-1',
        'D=M',
        '@LCL',
        'M=D',

        # Goto RET (goto return address)
        '@R14',
        'A=M',
        '0;JMP'
    ])



    def _write_code(self, code):
        self.output_file.write('\n'.join(code) + '\n')

    def close(self):
        self.output_file.close()
