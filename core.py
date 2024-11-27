from dataclasses import dataclass
from copy import deepcopy

frame_u = []

class Value:
    def __init__(self, literal = None, type: str = None):
        self.literal = literal if literal is not None else None
        self.type = type if type is not None else ""

    def matches(self, value: "Value"):
        return self.get() == value.get()

    def get(self):
        return self.literal

    def __str__(self):
        return f"{'{'}{self.type} {self.get()}{'}'}"

    def __repr__(self):
        if isinstance(self.literal, str):
            return f"Value('{self.literal}')"
        return f"Value({self.literal})"

class Facet:
    def __init__(self, name: str, value: Value):
        self.name = name
        self.value = value

    def matches(self, facet: "Facet"):
        return self.value.matches(facet.value) and self.name == facet.name

    def __str__(self):
        return f"[{self.name}: {self.value}]"

    def __repr__(self):
        return f"Facet('{self.name}', {self.value.__repr__()})"

@dataclass
class Rule:
    trigger: "Frame"
    effect: "Frame"
    priority: int = 1

class Frame:
    def __init__(self, name: str, *facets: "Facet"):
        self.name = name
        self.facets = list(facets)
        global frame_u
        frame_u.append(self)

    def matches(self, frame: "Frame"):
        """
        Checks if every facet matches it's corresponding facet in another frame
        :param frame:
        :return:
        """
        print(f"match {self} -> {frame}")

        for my_facet in self.facets:
            for other_facet in frame.facets:
                if other_facet.name == my_facet.name:
                    print(f"{my_facet} matches {other_facet}? ", end = "")
                    if not my_facet.matches(other_facet):
                        print("no")
                        return False
                    print("yes")
                    break # my_facet had a corresponding other_facet, go to next my_facet
            else: # If my_facet didn't have a corresponding other_facet
                print(f"{my_facet} had no matching facet")
                return False
        return True

    def add(self, facet: Facet):
        self.facets.append(facet)
    
    def get_value(self, facet_name: str):
        values = []
        for facet in self.facets:
            if facet.name == facet_name:
                values.append(facet.value)
        return values

    def __str__(self):
        return f"({self.name})"

    def __repr__(self):
        s =  f"Frame('{self.name}'"
        if self.facets:
            s += f", {", ".join(facet.__repr__() for facet in self.facets)})"
        else:
            s += ")"
        return s

def d(frame: Frame):
    """
    Describe a frame
    :param frame:
    :return:
    """
    print(frame)
    for facet in frame.facets:
        print("  ", end="")
        print(facet)

def r(n):
    print(n.__repr__())
    return n.__repr__()

class IntersectionValue(Value):
    def __init__(self, *values: Value):
        super().__init__(values, type = "Intersection")
    
    def matches(self, value: Value):
        for sub_value in self.literal:
            if not sub_value.matches(value):
                return False
        return True
    
    def __str__(self):
        return f"{'{'}{self.type} {" ".join(str(value) for value in self.get())}{'}'}"

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
    def __init__(self, literal):
        super().__init__(literal, "NumLessThan")

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


def find_matching_rules(frame: Frame, rules: list) -> list:
    """
    Find all rules that have a trigger matching the given frame.

    :param frame: The frame to match against rule triggers.
    :param rules: A list of Rule objects.
    :return: List of Rules whose triggers match the frame.
    """
    matching_rules = []
    for rule in rules:
        if rule.trigger.matches(frame) and not rule.effect.matches(frame):
            print(f"Frame {frame} matches trigger of Rule {rule}")
            matching_rules.append(rule)
    return matching_rules


def apply_effects(matching_rules: list, frame: Frame):
    """
    Apply the effects of all matching rules to the given frame.

    :param matching_rules: List of Rules whose effects will be applied.
    :param frame: The frame to which the effects will be applied.
    """
    for rule in matching_rules:
        print(f"Applying effect from Rule {rule} to Frame {frame}")
        for facet in rule.effect.facets:
            if isinstance(facet, FrameValueFacet):
                frame.add(Facet(name=facet.name, value=facet.value))
            else:
                frame.add(Facet(name=facet.name, value=deepcopy(facet.value)))


def infer(frame: Frame, rules: list):
    """
    The main inference function.

    :param frame: The initial frame to start with.
    :param rules: A list of Rule objects.
    """
    # Describe the initial frame
    d(frame)

    # Flag to indicate if any new effects were added in an iteration
    new_effects_applied = True

    while new_effects_applied:
        new_effects_applied = False

        # Find all matching rules for the current frame
        matching_rules = find_matching_rules(frame, rules)

        if not matching_rules:
            print("No more matching rules found.")
            break

        # Apply effects of matching rules to the frame
        apply_effects(matching_rules, frame)

        # If any new effects were added, we need to check again for matches
        if len(matching_rules) > 0:
            new_effects_applied = True

    # Describe the final frame after inference
    print("\nFinal Frame:")
    d(frame)


# Example usage
if __name__ == "__main__":
    # Create frames
    frame1 = Frame("Frame1", Facet("color", Value("red")), Facet("size", Value("large")))
    frame2 = Frame("Frame2", Facet("color", Value("blue")), Facet("size", Value("medium")))

    # Create rules
    rule1 = Rule(
        trigger=Frame("Trigger1", Facet("color", Value("red"))),
        effect=Frame("Effect1", Facet("shape", Value("square")))
    )

    rule2 = Rule(
        trigger=Frame("Trigger2", Facet("size", Value("large"))),
        effect=Frame("Effect2", Facet("material", Value("wood")))
    )

    # List of rules
    rules = [rule1, rule2]

    # Run inference on frame1 with the given rules
    infer(frame1, rules)