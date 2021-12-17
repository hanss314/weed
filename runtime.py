class Partial:
    def __init__(self, body, closure, arity, args):
        self.body = body
        self.closure = closure
        self.arity = arity
        self.args = args

    def __str__(self):
        return f'(|{",".join(map(str, self.closure))}|({",".join(map(str, self.args))})/{self.arity} -> {str(self.body)})'

