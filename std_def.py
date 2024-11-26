from core import Value, Frame

class AnyValue(Value):
    def matches(self, value: "Value"):
        return True

    def matches_fallback(self, value: "Value"):
        return True

class NumValue(Value):
    pass

class Relation(Value):
    def __init__(self, literal: Frame):
        super().__init__(literal)

    def matches_fallback(self, value: "Relation"):
        return self.get() is value.get()