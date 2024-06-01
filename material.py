import random
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

class Dielectric(Material):
    def __init__(self, refraction_index: float) -> None:
        super().__init__()
        self.refraction_index = refraction_index
    
    def scatter(self, r_in: Ray, rec: HitRecord) -> Tuple[Color, Ray]:
        ri = (1.0/self.refraction_index) if rec.front_face else self.refraction_index

        unit_direction = r_in.dir.normalize()
        
        cos_theta = min(-unit_direction.dot(rec.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta*cos_theta)

        cannot_refract = ri * sin_theta > 1.0

        if cannot_refract or self.__reflectance(cos_theta, ri) > random.random():
            direction = unit_direction.reflect(rec.normal)
        else: 
            direction = unit_direction.refract(rec.normal, ri)

        scattered = Ray(rec.p, direction)
        attenuation = Color(1.0, 1.0, 1.0)
        return attenuation, scattered
    
    def __reflectance(self, cosine: float, refraction_index: float):
        r0 = (1 - refraction_index) / (1 + refraction_index)
        r0 = r0 * r0
        return r0 + (1 - r0) * ((1 - cosine) ** 5)