import ast
import literals
import runtime
import random

def execute(statement_list):
    globs = {}
    for statement in statement_list:
        if isinstance(statement, ast.Let):
            handle_let(statement, globs, {}, globs)
        elif isinstance(statement, ast.Block):
            top_level_block(statement, globs)
        else:
            value = evaluate(statement, globs, {}, True)
            print(value)

def top_level_block(block, globs):
    scope = {}
    for statement in block.statements[:-1]:
        if isinstance(statement, ast.Let):
            handle_let(statement, globs, scope, scope)
        else:
            value = evaluate(statement, globs, scope, True)
            print(value)

    if block.statements:
        stmt = block.statements[-1]
        if isinstance(stmt, ast.Let):
            handle_let(stmt, globs, scope, globs)
        else:
            print(evaluate(stmt, globs, scope, True))


def handle_let(stmt, globs, scope, target):
    varnames = stmt.left
    values = stmt.right
    if len(varnames) != len(values):
        raise RuntimeError('Left and right of let expression have different lengths')
    
    new_dict = {}
    for name, value in zip(varnames, values):
        new_dict[name] = evaluate(value, globs, scope, stmt.eager)

    target |= new_dict

# TODO: replace this with proper builtin lookup table
def run_builtin(func, args, globs, scope):
    if func.name == '-': expected = [1,2]
    else: expected = [2]

    if len(args) not in expected:
        raise RuntimeError(f'{func} takes {expected} parameters')
    
    args = list(map(lambda x: evaluate(x, globs, scope, True), args))

    if func.name == '-' and len(args) == 1:
        return literals.Integer(-args[0].value)
    elif func.name == '-':
        return literals.Integer(args[0].value - args[1].value)
    elif func.name == '+':
        return literals.Integer(args[0].value + args[1].value)
    elif func.name == '*':
        return literals.Integer(args[0].value * args[1].value)
    elif func.name == '/':
        return literals.Integer(args[0].value // args[1].value)


# TODO: Refactor this to methods of classes
def evaluate(expr, globs, scope, eager=True):
    # TODO: calculate required closures and only copy the required values
    # TODO: do something smart here and replace scope with an array
    # This will likely require calculating the closures before runtime
    # and applying the calculated closures during evaluation
    if isinstance(expr, ast.Lambda):
        expr = runtime.Partial(expr.body, dict(scope), expr.args, [])
    elif not eager and not isinstance(expr, literals.Literal):
        return runtime.Partial(expr, dict(scope), [], [])

    if not eager: return expr

    if isinstance(expr, literals.Dice):
        return literals.Integer(random.randint(1, expr.max.value))

    elif isinstance(expr, literals.Literal):
        return expr

    elif isinstance(expr, literals.Identifier):
        if expr in scope: x = scope[expr]
        elif expr in globs: x = globs[expr]
        else: raise RuntimeError(f'{expr.name} not found')
        return evaluate(x, globs, scope, True)

    elif isinstance(expr, ast.FuncApp):
        func = evaluate(expr.func, globs, scope)
        args = list(map(lambda x: evaluate(x, globs, scope, False), expr.args))
        
        if isinstance(func, literals.Integer) and not args:
            return func
        if isinstance(func, literals.Integer):
            total = 0
            for _ in range(func.value):
                total += evaluate(expr.args[0], globs, scope, True).value
            return evaluate(ast.FuncApp(literals.Integer(total), args[1:]), globs, scope, True)

        elif isinstance(func, literals.Builtin):
            return run_builtin(func, args, globs, scope)

        elif not isinstance(func, runtime.Partial):
            raise RuntimeError(f'{expr.func} is not a function object')
        
        if not args: return func;

        func = runtime.Partial(func.body, func.closure, func.arity, func.args+args)
        return evaluate(func, globs, scope)

    elif isinstance(expr, runtime.Partial):
        if len(expr.args) >= len(expr.arity):
            arity = len(expr.arity)
            clos = dict(expr.closure)
            old_args = expr.args[:arity]
            new_args = expr.args[arity:]
            for name, value in zip(expr.arity, old_args):
                clos[name] = value

            result = evaluate(expr.body, globs, clos, True)
            if not new_args: return result
            return evaluate(ast.FuncApp(result, new_args), globs, clos, True)
        else:
            return expr

    elif isinstance(expr, ast.If):
        cond = evaluate(expr.cond, globs, scope, True)
        return evaluate(expr.pos if cond.value else expr.neg, globs, scope, True)

    elif isinstance(expr, ast.Block):
        new_scope = dict(scope)
        curr = None
        for n, stmt in enumerate(expr.statements):
            if isinstance(stmt, ast.Let):
                if n == len(expr.statements)-1:
                    handle_let(stmt, globs, new_scope, scope)
                else:
                    handle_let(stmt, globs, new_scope, new_scope)

            elif isinstance(stmt, ast.Return):
                return evaluate(stmt.statement, globs, new_scope, True)
            else:
                curr = evaluate(stmt, globs, new_scope, True)

        return curr 

