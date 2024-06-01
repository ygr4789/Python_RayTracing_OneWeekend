from vec3 import Point3, Vec3

class Ray:
    def __init__(self, origin: Point3, direction: Vec3):
        self.dir = direction
        self.orig = origin
        
    def at(self, t: float):
        return self.orig + self.dir * t