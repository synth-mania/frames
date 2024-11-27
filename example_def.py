from core import *

class Age(NumValueFacet):
    def __init__(self, literal):
        super().__init__("Age", literal)

class Sex(StringValueFacet):
    def __init__(self, literal):
        super().__init__("Sex", literal)
