from ray import *
from interval import *

class HitRecord:
    def __init__(self) -> None:
        self.p: Point3
        self.normal: Vec3
        self.t: float
        self.front_face: bool
        
    def set_face_normal(self, r: Ray, outward_normal: Vec3) -> None:
        """
        Sets the hit record normal vector.
        NOTE: the parameter `outward_normal` is assumed to have unit length.
        """

        self.front_face = r.dir.dot(outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal

class Hittable:
    def hit(self, r: Ray, ray_t: Interval) -> HitRecord:
        raise NotImplementedError()