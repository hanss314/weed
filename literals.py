import runtime

# These should be immutable
class Literal:
    def generate_runtime(self, closure, arguments):
        return self

class Integer(Literal):
    def __init__(self, value=0):
        self._value = int(value)

    @property
    def value(self):
        return self._value

    def __str__(self):
        return str(self._value)

class Floating(Literal):
    def __init__(self, value=0.0):
        self._value = float(value)

    @property
    def value(self):
        return self._value
    
    def __str__(self):
        return str(self._value)

class String(Literal):
    def __init__(self, value=""):
        self._value = value

    @property
    def value(self):
        return self._value
    
    def __str__(self):
        return repr(self._value)

class Bool(Literal):
    def __init__(self, value=False):
        self._value = value

    @property
    def value(self):
        return self._value
    
    def __str__(self):
        return str(self._value)

class Identifier:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name
    
    def __str__(self):
        return self._name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

class Dice:
    def __init__(self, m):
        self.max = m
    
    def __str__(self):
        return f"d{self.max}"

class Builtin(Literal):
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name
