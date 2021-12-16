class Let:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        return f'let ({",".join(map(str, self.left))}) = ({",".join(map(str,self.right))})'

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

class Block:
    def __init__(self, statements):
        self.statements = statements

    def __str__(self):
        return '{\n' + f'{chr(10).join(map(str, self.statements))}' + '\n}'

class Return:
    def __init__(self, statement):
        self.statement = statement

    def __str__(self):
        return f'return {self.statement}'
