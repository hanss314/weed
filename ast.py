from pyparsing import ParseException
import runtime

class Let:
    def __init__(self, left, right, eager=True):
        self.left = left
        self.right = right
        self.eager = eager
    
    def __str__(self):
        typ = 'let' if self.eager else 'fun'
        return f'{typ} ({",".join(map(str, self.left))}) = ({",".join(map(str,self.right))})'

class Lambda:
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def __str__(self):
        return f'({",".join(map(str, self.args))}) -> {str(self.body)}'

class FuncApp:
    def __init__(self, func, args):
        self.func = func
        self.args = args
    
    def __str__(self):
        return f'{self.func}({",".join(map(str, self.args))})'

    def __repr__(self):
        return str(self)

class Block:
    def __init__(self, statements):
        if statements and isinstance(statements[-1], Block):
            self.statements = statements[:-1] + statements[-1].statements
        else:
            self.statements = statements

    def __str__(self):
        return '{\n' + f'{chr(10).join(map(str, self.statements))}' + '\n}'

class Return:
    def __init__(self, statement):
        self.statement = statement

    def __str__(self):
        return f'return {self.statement}'

class If:
    def __init__(self, cond, pos, neg):
        self.cond = cond
        self.pos = pos
        self.neg = neg

    def __str__(self):
        return f'if {self.cond} then {self.pos} else {self.neg}'
