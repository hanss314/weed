import parse
import evaluation
from sys import argv

tree = parse.program.parse_string(open(argv[1], 'r').read(), parse_all=True)
evaluation.execute(tree)
