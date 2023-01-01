import sys
from enum import Enum

TokenType = Enum("TokenType", ['LEFT_PAREN', 'RIGHT_PAREN', 'LEFT_BRACE', 'RIGHT_BRACE', 'COMMA', 'DOT', 'MINUS', 'PLUS', 'SEMICOLON', 'SLASH', 'STAR', 'BANG', 'BANG_EQUAL', 'EQUAL', 'EQUAL_EQUAL', 'GREATER', 'GREATER_EQUAL', 'LESS', 'LESS_EQUAL', 'IDENTIFIER', 'STRING', 'NUMBER', 'AND', 'CLASS', 'ELSE', 'FALSE', 'FUN', 'FOR', 'IF', 'NIL', 'OR', 'PRINT', 'RETURN', 'SUPER', 'self', 'TRUE', 'VAR', 'WHILE', 'EOF'])

class Token:
    def __init__(self, type_, lexeme: str, literal, line):
        self.type_ = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def toString(self):
        return f"{self.type} {self.lexeme} {self.literal}"

class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scanTokens(self):
        while not self.isAtEnd():
            start = self.current
            self.scanToken()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
    
    def isAtEnd(self):
        return self.current >= len(self.source)
    
    def scanToken(self):
        c = self.advance()
        switch_dict_1 = {
                "(": TokenType.LEFT_PAREN,
                ")": TokenType.RIGHT_PAREN,
                "{": TokenType.LEFT_BRACE,
                "}": TokenType.RIGHT_BRACE,
                ",": TokenType.COMMA,
                ".": TokenType.DOT,
                "-": TokenType.MINUS,
                "+": TokenType.PLUS,
                ";": TokenType.SEMICOLON,
                "*": TokenType.STAR
                }

        if c in switch_dict_1.keys():
            self.addToken(switch_dict_1[c])
        elif c == "!":
            self.addToken(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
        elif c == "=":
            self.addToken(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL)
        elif c == "<":
            self.addToken(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
        elif c == ">":
            self.addToken(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)
        elif c == "/":
            if self.match("/"):
                while (self.peek() != "\n" and not self.isAtEnd()):
                    _ = self.advance()
            else:
                self.addToken1(TokenType.SLASH)
        elif c in [" ", "\r", "\t"]:
            pass
        elif c == "\n":
            self.line += 1
            pass

        else:
            Lox.error(self.line, "Unexpected character.")
    
    def match(self, expected):
        if self.isAtEnd():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self):
        if self.isAtEnd():
            return "\0"
        return self.source[self.current]

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def addToken1(self, type_):
        self.addToken2(type_, None)

    def addToken2(self, type_, literal):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type_, text, literal, self.line))

class Lox:
    def __init__(self):
        self.hadError = False

    @classmethod
    def main(self):
        args = sys.argv
        args.pop(0)

        if len(args) > 1:
            print("Usage: jlox [script]")
            exit()
        elif len(args) == 1:
            self.runFile(args[0])
        else:
            self.runPrompt()

    def runFile(self, path: str):
        try:
            bytes_ = open(path, "r")
            self.run(bytes_)
        except:
            raise Exception("IOException")

    def runPrompt(self):
        try:
            while True:
                line = input("> ")
                if line == "":
                    break
                self.run(line);
                self.hadError = False
        except:
            raise Exception("IOException")

    def run(self, source: str):
        scanner = Scanner(source);
        tokens = scanner.scanTokens();

        for token in tokens:
            print(token)
        
        if self.hadError:
            exit()

    @classmethod
    def error(self, line: int, message: str):
        self.report(line, "", message);

    def report(self, line: int, where: str, message: str):
        print(f"[line " + line + "] Error" + where + ": " + message)
        hadError = True


Lox.main()