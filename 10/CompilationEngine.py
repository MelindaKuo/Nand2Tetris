class CompilationEngine:
    def __init__(self, tokenizer, output_file):
        self.tokenizer = tokenizer
        self.output_file = open(output_file, 'w')
        self.indentation_level = 0

    def write(self, text):
        self.output_file.write('  ' * self.indentation_level + text + '\n')

    def advance_and_write(self):
        self.tokenizer.advance()
        token_type = self.tokenizer.token_type()
        
        if token_type == "KEYWORD":
            self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")
        elif token_type == "SYMBOL":
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")
        elif token_type == "IDENTIFIER":
            self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")
        elif token_type == "INT_CONST":
            self.write(f"<integerConstant> {self.tokenizer.int_val()} </integerConstant>")
        elif token_type == "STRING_CONST":
            self.write(f"<stringConstant> {self.tokenizer.string_val()} </stringConstant>")

    def compileClass(self):
        self.write("<class>")
        self.indentation_level += 1

        self.advance_and_write()  # 'class'
        self.advance_and_write()  # className
        self.advance_and_write()  # '{'

        while self.tokenizer.keyword() in ("static", "field"):
            self.compileClassVarDec()

        while self.tokenizer.keyword() in ("constructor", "function", "method"):
            self.compileSubroutine()

        self.advance_and_write()  # '}'

        self.indentation_level -= 1
        self.write("</class>")

    def compileClassVarDec(self):
        self.write("<classVarDec>")
        self.indentation_level += 1

        self.advance_and_write()  # 'static' | 'field'
        self.advance_and_write()  # type
        self.advance_and_write()  # varName

        while self.tokenizer.symbol() == ',':
            self.advance_and_write()  # ','
            self.advance_and_write()  # varName

        self.advance_and_write()  # ';'

        self.indentation_level -= 1
        self.write("</classVarDec>")

    def compileSubroutine(self):
        self.write("<subroutineDec>")
        self.indentation_level += 1

        self.advance_and_write()  # 'constructor' | 'function' | 'method'
        self.advance_and_write()  # 'void' | type
        self.advance_and_write()  # subroutineName
        self.advance_and_write()  # '('

        self.compileParameterList()

        self.advance_and_write()  # ')'

        self.write("<subroutineBody>")
        self.indentation_level += 1

        self.advance_and_write()  # '{'

        while self.tokenizer.keyword() == "var":
            self.compileVarDec()

        self.compileStatements()

        self.advance_and_write()  # '}'

        self.indentation_level -= 1
        self.write("</subroutineBody>")

        self.indentation_level -= 1
        self.write("</subroutineDec>")

    def compileParameterList(self):
        self.write("<parameterList>")
        self.indentation_level += 1

        if self.tokenizer.token_type() != "SYMBOL":  # check for non-empty parameter list
            self.advance_and_write()  # type
            self.advance_and_write()  # varName

            while self.tokenizer.symbol() == ',':
                self.advance_and_write()  # ','
                self.advance_and_write()  # type
                self.advance_and_write()  # varName

        self.indentation_level -= 1
        self.write("</parameterList>")

    def compileVarDec(self):
        self.write("<varDec>")
        self.indentation_level += 1

        self.advance_and_write()  # 'var'
        self.advance_and_write()  # type
        self.advance_and_write()  # varName

        while self.tokenizer.symbol() == ',':
            self.advance_and_write()  # ','
            self.advance_and_write()  # varName

        self.advance_and_write()  # ';'

        self.indentation_level -= 1
        self.write("</varDec>")

    def compileStatements(self):
        self.write("<statements>")
        self.indentation_level += 1

        while self.tokenizer.keyword() in {"let", "if", "while", "do", "return"}:
            if self.tokenizer.keyword() == "let":
                self.compileLet()
            elif self.tokenizer.keyword() == "if":
                self.compileIf()
            elif self.tokenizer.keyword() == "while":
                self.compileWhile()
            elif self.tokenizer.keyword() == "do":
                self.compileDo()
            elif self.tokenizer.keyword() == "return":
                self.compileReturn()

        self.indentation_level -= 1
        self.write("</statements>")

    def compileLet(self):
        self.write("<letStatement>")
        self.indentation_level += 1

        self.advance_and_write()  # 'let'
        self.advance_and_write()  # varName

        if self.tokenizer.symbol() == '[':
            self.advance_and_write()  # '['
            self.compileExpression()
            self.advance_and_write()  # ']'

        self.advance_and_write()  # '='
        self.compileExpression()
        self.advance_and_write()  # ';'

        self.indentation_level -= 1
        self.write("</letStatement>")

    def compileIf(self):
        self.write("<ifStatement>")
        self.indentation_level += 1

        self.advance_and_write()  # 'if'
        self.advance_and_write()  # '('
        self.compileExpression()
        self.advance_and_write()  # ')'

        self.advance_and_write()  # '{'
        self.compileStatements()
        self.advance_and_write()  # '}'

        if self.tokenizer.keyword() == "else":
            self.advance_and_write()  # 'else'
            self.advance_and_write()  # '{'
            self.compileStatements()
            self.advance_and_write()  # '}'

        self.indentation_level -= 1
        self.write("</ifStatement>")

    def compileWhile(self):
        self.write("<whileStatement>")
        self.indentation_level += 1

        self.advance_and_write()  # 'while'
        self.advance_and_write()  # '('
        self.compileExpression()  # expression
        self.advance_and_write()  # ')'
        self.advance_and_write()  # '{'
        self.compileStatements()  # statements
        self.advance_and_write()  # '}'

        self.indentation_level -= 1
        self.write("</whileStatement>")
    
    def compileDo(self):
        self.write("<doStatement>")
        self.indentation_level += 1

        self.advance_and_write()  # 'do'
        self.advance_and_write()  # subroutineName or className

        if self.tokenizer.symbol() == '.':
            self.advance_and_write()  # '.'
            self.advance_and_write()  # subroutineName

        self.advance_and_write()  # '('
        self.compileExpressionList()  # expressionList
        self.advance_and_write()  # ')'
        self.advance_and_write()  # ';'

        self.indentation_level -= 1
        self.write("</doStatement>")
    
    def compileReturn(self):
        self.write("<returnStatement>")
        self.indentation_level += 1

        self.advance_and_write()  # 'return'

        # Check if there's an expression to return
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ';':
            self.compileExpression()

        self.advance_and_write()  # ';'

        self.indentation_level -= 1
        self.write("</returnStatement>")
    
    def compileSubroutineBody(self):
        self.write("<subroutineBody>")
        self.indentation_level += 1

        self.advance_and_write()  # '{'

        # Handle variable declarations (varDec*)
        while self.tokenizer.keyword() == "var":
            self.compileVarDec()

        # Handle the statements within the subroutine
        self.compileStatements()

        self.advance_and_write()  # '}'

        self.indentation_level -= 1
        self.write("</subroutineBody>")






    def compileTerm(self):
        self.write("<term>")
        self.indentation_level += 1

        token_type = self.tokenizer.token_type()

        if token_type == "INT_CONST":
            self.advance_and_write()  # integer constant
        elif token_type == "STRING_CONST":
            self.advance_and_write()  # string constant
        elif token_type == "KEYWORD":
            if self.tokenizer.keyword() in {"true", "false", "null", "this"}:
                self.advance_and_write()  # keyword constant
        elif token_type == "IDENTIFIER":
            self.advance_and_write()  # varName or subroutineName or className
            
            if self.tokenizer.symbol() == '[':  # array indexing
                self.advance_and_write()  # '['
                self.compileExpression()
                self.advance_and_write()  # ']'
            elif self.tokenizer.symbol() == '(':  # subroutine call (methodName(args))
                self.advance_and_write()  # '('
                self.compileExpressionList()
                self.advance_and_write()  # ')'
            elif self.tokenizer.symbol() == '.':  # subroutine call (className.methodName(args))
                self.advance_and_write()  # '.'
                self.advance_and_write()  # subroutineName
                self.advance_and_write()  # '('
                self.compileExpressionList()
                self.advance_and_write()  # ')'
        elif self.tokenizer.symbol() == '(':
            self.advance_and_write()  # '('
            self.compileExpression()
            self.advance_and_write()  # ')'
        elif self.tokenizer.symbol() in {'-', '~'}:  # unary operators
            self.advance_and_write()  # unary operator
            self.compileTerm()

        self.indentation_level -= 1
        self.write("</term>")
    
    def compileExpressionList(self):
        self.write("<expressionList>")
        self.indentation_level += 1

        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ')':
            self.compileExpression()

            while self.tokenizer.symbol() == ',':
                self.advance_and_write()  # ','
                self.compileExpression()

        self.indentation_level -= 1
        self.write("</expressionList>")


    

    def close(self):
        self.output_file.close()
