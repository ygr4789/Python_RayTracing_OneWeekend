from typing import Tuple

from hittable import *

class Material:
    def scatter(self, r_in: Ray, rec: HitRecord) -> Tuple[Color, Ray]:
        return None, None
    
class Lambertian(Material):
    def __init__(self, albedo: Color) -> None:
        super().__init__()
        self.albedo = albedo
    
    def scatter(self, r_in: Ray, rec: HitRecord) -> Tuple[Color, Ray]:
        scatter_direction = rec.normal + Vec3.rand_unit_vector()
        if scatter_direction.near_zero():
            scatter_direction = rec.normal
            
        scattered = Ray(rec.p, scatter_direction)
        attenuation = self.albedo
        return attenuation, scattered
    
class Metal(Material):
    def __init__(self, albedo: Color, fuzz: float) -> None:
        super().__init__()
        self.albedo = albedo
        self.fuzz = min(fuzz, 1)
    
    def scatter(self, r_in: Ray, rec: HitRecord) -> Tuple[Color, Ray]:
        reflected = r_in.dir.reflect(rec.normal) + Vec3.rand_unit_vector() * self.fuzz
        
        scattered = Ray(rec.p, reflected)
        attenuation = self.albedo
        if scattered.dir.dot(rec.normal) <= 0: return None, None
        return attenuation, scattered
    