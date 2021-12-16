# These should be immutable
class Integer:
    def __init__(self, value=0):
        self._value = int(value)

    @property
    def value(self):
        return self._value

    def __str__(self):
        return str(self._value)

class Floating:
    def __init__(self, value=0.0):
        self._value = float(value)

    @property
    def value(self):
        return self._value
    
    def __str__(self):
        return str(self._value)

class String:
    def __init__(self, value=""):
        self._value = value

    @property
    def value(self):
        return self._value
    
    def __str__(self):
        return repr(self._value)

class Bool:
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

class Dice:
    def __init__(self, m):
        self.max = m
    
    def __str__(self):
        return f"d{self.max}"

class Builtin:
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name
