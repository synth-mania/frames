from core import *
from std_def import *

class Location(Facet):
    def __init__(self, literal):
        super().__init__("Location", Relation(literal))

class HasComponent(Facet):
    def __init__(self, literal):
        super().__init__("HasComponent", Relation(literal))