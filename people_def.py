from core import *
from std_def import *

class Age(Facet):
    def __init__(self, literal):
        super().__init__("Age", Value(literal))

class Sex(Facet):
    def __init__(self, literal):
        super().__init__("Sex", Value(literal))