import math

from hittable import *
from material import Material

class Sphere(Hittable):
    def __init__(self, center: Point3, radius: float, mat: Material) -> None:
        super().__init__()
        self.center = center
        self.radius = max(0.0, radius)
        self.mat = mat
        
    def hit(self, r: Ray, ray_t: Interval) -> HitRecord:
        oc = self.center - r.orig
        a = r.dir.mag_sq
        h = r.dir.dot(oc)
        c = oc.mag_sq - self.radius ** 2
        
        discriminant = h*h - a*c
    
        if discriminant < 0: return None

        sqrtd = math.sqrt(discriminant)

        # Find the nearest root that lies in the acceptable range.
        root = (h - sqrtd) / a
        if not ray_t.surrounds(root):
            root = (h + sqrtd) / a
            if not ray_t.surrounds(root): return None

        rec = HitRecord()
        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        rec.mat = self.mat
        
        return rec