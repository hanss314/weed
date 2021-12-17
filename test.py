import parse
import evaluation

evaluation.execute(parse.program.parse_string(open('program.wd', 'r').read(), parse_all=True))
