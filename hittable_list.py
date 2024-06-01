from typing import List

from hittable import *

class HittableList(Hittable):
    def __init__(self) -> None:
        super().__init__()
        self.objects: List[Hittable] = []

    def clear(self):
        self.objects.clear()
        
    def add(self, object: Hittable):
        self.objects.append(object)

    def hit(self, r: Ray, ray_t: Interval) -> HitRecord:
        rec = None
        closest_so_far = ray_t.max

        for object in self.objects:
            if tmp_rec := object.hit(r, Interval(ray_t.min, closest_so_far)):
                rec = tmp_rec
                closest_so_far = rec.t

        return rec