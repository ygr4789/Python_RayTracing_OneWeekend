import math

class Interval:
    def __init__(self, min = math.inf, max = -math.inf) -> None:
        self.min = min
        self.max = max
        
    @property
    def size(self):
        return self.max - self.min
    
    def contains(self, x: float) -> bool:
        return self.min <= x <= self.max
    
    def surrounds(self, x: float) -> bool:
        return self.min < x < self.max

empty = Interval(math.inf, -math.inf)
universe = Interval(-math.inf, math.inf)