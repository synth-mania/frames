from core import *
from std_def import *

class Location(Facet):
    def __init__(self, literal):
        super().__init__("Location", FrameValue(literal))

class HasComponent(Facet):
    def __init__(self, literal):
        super().__init__("HasComponent", FrameValue(literal))