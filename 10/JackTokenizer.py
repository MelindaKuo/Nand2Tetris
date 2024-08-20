import re

class JackTokenizer:

    KEYWORDS = {
        "class", "constructor", "function", "method", "field", "static", "var", 
        "int", "char", "boolean", "void", "true", "false", "null", "this", 
        "let", "do", "if", "else", "while", "return"
    }
    
    SYMBOLS = {
        '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', 
        '|', '<', '>', '=', '~'
    }

    # Token types
    TOKEN_TYPES = {
        "KEYWORD": "KEYWORD",
        "SYMBOL": "SYMBOL",
        "IDENTIFIER": "IDENTIFIER",
        "INT_CONST": "INT_CONST",
        "STRING_CONST": "STRING_CONST"
    }


    def __init__(self, input_file):
        with open(input_file, 'r') as file:
            self.input_data = file.read()
        
        self.tokens = []
        self.current_token = None
        self.current_index = -1
        
        self._remove_comments()
        self._tokenize()

    def hasMoreTokens(self):
        return self.current_index +1<len(self.tokens)
    
    def advance(self):
        if self.hasMoreTokens():
            self.current_index+=1
            self.current_token=self.tokens[self.current_index]

    def tokenType(self):
        if self.current_token in JackTokenizer.KEYWORDS:
            return JackTokenizer.TOKEN_TYPES["KEYWORD"]
        elif self.current_token in JackTokenizer.SYMBOLS:
            return JackTokenizer.TOKEN_TYPES["SYMBOL"]
        elif self.current_token.isdigit():
            return JackTokenizer.TOKEN_TYPES["INT_CONST"]
        elif self.current_token.startswith('"'):
            return JackTokenizer.TOKEN_TYPES["STRING_CONST"]
        else:
            return JackTokenizer.TOKEN_TYPES["IDENTIFIER"]

    def keyword(self):
    if self.token_type() == JackTokenizer.TOKEN_TYPES["KEYWORD"]:
        return self.current_token
    return None

    def symbol(self):
        if self.token_type() == JackTokenizer.TOKEN_TYPES["SYMBOL"]:
            return self.current_token
        return None

    def identifier(self):
        if self.token_type() == JackTokenizer.TOKEN_TYPES["IDENTIFIER"]:
            return self.current_token
        return None

    def int_val(self):
        if self.token_type() == JackTokenizer.TOKEN_TYPES["INT_CONST"]:
            return int(self.current_token)
        return None

    def string_val(self):
        if self.token_type() == JackTokenizer.TOKEN_TYPES["STRING_CONST"]:
            return self.current_token[1:-1] 
        return None
        