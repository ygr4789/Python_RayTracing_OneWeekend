from vec3 import *

class Ray:
    def __init__(self, origin: Point3, direction: Vec3) -> None:
        self.dir = direction
        self.orig = origin
        
    def at(self, t: float):
        return self.orig + self.dir * t