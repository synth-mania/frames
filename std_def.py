from core import Value, Frame, Facet

class AnyValue(Value):
    def matches(self, value: "Value"):
        return True

class StringValue(Value):
    def __init__(self, literal, type="String"):
        super().__init__(literal, type)

class NumValue(Value):
    def __init__(self, literal, type = "num"):
        super().__init__(literal, type)

class NumGreaterThanValue(NumValue):
    def __init__(self, literal):
        super().__init__(literal, "NumGreaterThan")

    def matches(self, value: "NumValue"):
        if not isinstance(value, NumValue):
            raise ValueError("NumGreaterThanValue can only be applied to NumValue types")
        return value.get() > self.get()

class NumLessThanValue(NumValue):
    def matches(self, value: "NumValue"):
        if not isinstance(value, NumValue):
            raise ValueError("NumGreaterThanValue can only be applied to NumValue types")
        return value.get() < self.get()

class FrameValue(Value):
    def __init__(self, literal: Frame, type = "Relation"):
        super().__init__(literal, type)

    def matches(self, value: "FrameValue"):
        return self.get() is value.get()

class NumValueFacet(Facet):
    def __init__(self, name, literal):
        if not(isinstance(literal, float) or isinstance(literal, int)):
            super().__init__(name, literal)
        else:
            super().__init__(name, NumValue(literal))

class StringValueFacet(Facet):
    def __init__(self, name, literal):
        if not(isinstance(literal, str)):
            super().__init__(name, literal)
        else:
            super().__init__(name, StringValue(literal))

class FrameValueFacet(Facet):
    def __init__(self, name, literal):
        if not(isinstance(literal, Frame)):
            super().__init__(name, literal)
        else:
            super().__init__(name, FrameValue(literal))