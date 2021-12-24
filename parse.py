from pyparsing import *
import literals
import ast

ParserElement.set_default_whitespace_chars(" \t")

RESERVED = [
    "@", ".", "**", "*", "/", "//", "%", "+", "-", 
    "=", "!=", ">", ">=", "<", "<=", 
    '&', '^', '|', '&&', '||', '$',
    'let', 'fun', 'fix', 'return', 'in', 'if', 'then', 'else',
]

LPAR, RPAR = map(Suppress, "()")
LBRACE, RBRACE = map(Suppress, "{}")
EQUALS = Suppress('=')

LET = Keyword('let')
FIX= Keyword('fix')

FUN = Suppress(Keyword('fun'))
IN = Suppress(Keyword('in'))
RETURN = Suppress(Keyword('return'))
LAMBDA = Suppress("->")
IF = Suppress(Keyword('if'))
THEN = Suppress(Keyword('then'))
ELSE = Suppress(Keyword('else'))

LINE_SEP = Suppress(OneOrMore(Literal(';') | Literal('\n')))

def non_reserved_id(tok):
    tok = tok[0]
    if tok in RESERVED:
        raise ParseException(f"{tok} is a reserved function")
    return literals.Identifier(tok)

def func_app(tok):
    return ast.FuncApp(tok[0], tok[1:])

def binop(tok):
    tok = tok[0]
    curr = ast.FuncApp(literals.Builtin(tok[1]), [tok[0], tok[2]])
    for i in range(3, len(tok), 2):
        curr = ast.FuncApp(literals.Builtin(tok[i]), [curr, tok[i+1]])

    return curr

def let_stmt_action(tok):
    var = tok[1]
    bindings = tok[2] if tok[0] == "let" else tok[1]
    return ast.Let(var, bindings)

def let_expr_action(tok):
    return ast.Block([tok[0], tok[1]])

def function_action(tok):
    return ast.Let([tok[0]], [ast.Lambda(tok[1], tok[2])], False)

def lambda_action(tok):
    return ast.Lambda(tok[0], tok[1])

expression = Forward()
statement = Forward()

alpha_id = Regex(r'[a-zA-Z_]+')
symbo_id = Regex(r'[!@#$%^&*+=:|?/<>~`][!@#$%^&*+=:|?/<>~`\-]*')
identifier = (alpha_id | symbo_id).set_parse_action(non_reserved_id)

integer_lit = Regex(r'([1-9][0-9]*)|0').set_parse_action(lambda tok: literals.Integer(tok[0]))
literal = integer_lit

paren_expr = LPAR + expression + RPAR

arith_atom = paren_expr | literal | identifier

dice_n = ("d"+arith_atom.leave_whitespace(False)).set_parse_action(lambda tok: literals.Dice(tok[1]))
# TODO: replace this with a proper full-fledged dice notation
dice = dice_n

atom = dice | arith_atom

funcapp = atom + OneOrMore(LPAR + Optional(delimited_list(expression)) + RPAR)
funcapp.set_parse_action(func_app)

arith_expr = infix_notation(funcapp | atom, [
    ('-', 1, OpAssoc.RIGHT, lambda tok: ast.FuncApp(literals.Builtin('neg'), [tok[0][1]])),
    (one_of('* /'), 2, OpAssoc.LEFT, binop),
    (one_of('+ -'), 2, OpAssoc.LEFT, binop),
])

id_tuple = LPAR + identifier + Optional(Suppress(",") + delimited_list(identifier)) + RPAR
expr_tuple = LPAR + expression + Optional(Suppress(",") + delimited_list(expression)) + RPAR

single_let = LET + Group(identifier) + EQUALS + Group(expression)
multi_let = LET + Group(id_tuple) + EQUALS + Group(expr_tuple)
single_fix = FIX + Group(identifier)
multi_fix = FIX + Group(id_tuple)

fun_stmt = Forward()

let_header = multi_let | single_let | single_fix | multi_fix
let_list = delimited_list(let_header, delim=IN) 
let_stmt = (let_list + Optional(IN+fun_stmt)).set_parse_action(ast.Block)
let_expr = (let_list + IN + expression).set_parse_action(ast.Block)

let_header.set_parse_action(let_stmt_action)
#let_expr.set_parse_action(let_expr_action)

return_stmt = (RETURN + expression).set_parse_action(lambda tok: ast.Return(tok[0]))

expr_block_stmt = statement | return_stmt
expr_block = LBRACE + Suppress(ZeroOrMore('\n')) + \
    Optional(
            delimited_list(expr_block_stmt + FollowedBy(LINE_SEP + expr_block_stmt), delim=LINE_SEP) + \
            Suppress(OneOrMore(LINE_SEP))
    ) + \
    (return_stmt | expression) + Suppress(ZeroOrMore(LINE_SEP)) + RBRACE
expr_block.set_parse_action(ast.Block)

fun_header = FUN + identifier + Group(Optional(LPAR + Optional(delimited_list(identifier)) + RPAR))
fun_stmt << ((fun_header + EQUALS + expression) | (fun_header + expr_block))
fun_stmt.set_parse_action(function_action)

sub_lamb = (let_expr | arith_expr | expr_block)
lamb = Forward()
id_or_list = identifier | (LPAR + Optional(delimited_list(identifier)) + RPAR)
lamb << ((Group(id_or_list) + LAMBDA + lamb).set_parse_action(lambda_action) | sub_lamb)

if_subexpr = lamb
if_expr = IF + if_subexpr + THEN + if_subexpr + ELSE + if_subexpr
if_expr.set_parse_action(lambda toks: ast.If(*toks))

expression << (lamb | if_expr)
statement << (expression | let_stmt | fun_stmt)


top_block = LBRACE + Suppress(ZeroOrMore('\n')) + \
    delimited_list(statement, delim=LINE_SEP, allow_trailing_delim=True) + RBRACE
top_block.set_parse_action(ast.Block)



program = Suppress(ZeroOrMore('\n')) + delimited_list(top_block | statement, delim=LINE_SEP, allow_trailing_delim=True)
