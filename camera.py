import random
from tqdm import tqdm

from hittable import *
from interval import *

def _linear_to_gamma(linear_component: float) -> float:
    if linear_component > 0: return math.sqrt(linear_component)
    else: return 0

def _write_color(target: list, c: Color) -> None:
    r = _linear_to_gamma(c.x)
    g = _linear_to_gamma(c.y)
    b = _linear_to_gamma(c.z)
    
    intensity = Interval(0, 0.999)
    r = int(256 * intensity.clamp(r))
    g = int(256 * intensity.clamp(g))
    b = int(256 * intensity.clamp(b))
    target.extend([r, g, b])

class Camera:
    def __init__(
        self, 
        aspect_ratio:float = 1.0, 
        image_width:int = 100, 
        samples_per_pixel:int = 10,
        max_depth:int = 1,
        vfov:float = 90
    ) -> None:
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
        self.samples_per_pixel = samples_per_pixel
        self.max_depth = max_depth
        self.vfov = vfov
        
        self.lookfrom = Point3(0,0,0)
        self.lookat = Point3(0,0,-1)
        self.vup = Vec3(0,1,0)
        
        self.__image_height: int
        self.__center: Point3
        self.__pixel00_loc: Point3
        self.__pixel_delta_u: Vec3
        self.__pixel_delta_v: Vec3
    
    def render(self, world:Hittable, target:list) -> None:
        self.__initialize()
        pbar = tqdm(total=self.__image_height*self.image_width)
        
        for v in range(self.__image_height):
            for u in range(self.image_width):
                pixel_color = Color(0, 0, 0)
                for _ in range(self.samples_per_pixel):
                    r = self.__get_ray(u, v)
                    pixel_color += self.__ray_color(r, self.max_depth, world)
                pixel_color /= self.samples_per_pixel
                _write_color(target, pixel_color)
                pbar.update(1)
    
    def __initialize(self) -> None:
        image_width = self.image_width
        image_height = int(image_width / self.aspect_ratio)
        
        center = self.lookfrom
        
        focal_length = (self.lookfrom - self.lookat).mag
        theta = math.radians(self.vfov)
        h = math.tan(theta/2)
        viewport_height = 2 * h * focal_length
        viewport_width = viewport_height * (image_width/image_height)

        w = (self.lookfrom - self.lookat).normalize()
        u = self.vup.cross(w).normalize()
        v = w.cross(u)

        viewport_u = u * viewport_width
        viewport_v = -v * viewport_height

        pixel_delta_u = viewport_u / image_width
        pixel_delta_v = viewport_v / image_height

        viewport_upper_left = center - (w * focal_length) - viewport_u/2 - viewport_v/2
        pixel00_loc = viewport_upper_left + (pixel_delta_u + pixel_delta_v) * 0.5
        
        self.__image_height = image_height
        self.__center = center
        self.__pixel_delta_u = pixel_delta_u
        self.__pixel_delta_v = pixel_delta_v
        self.__pixel00_loc = pixel00_loc
    
    def __get_ray(self, u:int, v:int) -> Ray:
        offset = self.__sample_square()
        pixel_sample = self.__pixel00_loc + (self.__pixel_delta_u * (u + offset.x)) + (self.__pixel_delta_v * (v + offset.y))
        ray_origin = self.__center
        ray_direction = pixel_sample - ray_origin
        return Ray(ray_origin, ray_direction)
        
    def __sample_square(self) -> Vec3:
        return Vec3(random.random() - 0.5, random.random() - 0.5, 0)
    
    def __ray_color(self, r:Ray, depth:int, world:Hittable) -> Color:
        if depth <= 0:
            return Color(0, 0, 0)
        
        if rec := world.hit(r, Interval(0.001, math.inf)):
            attenuation, scattered = rec.mat.scatter(r, rec)
            if scattered:
                return attenuation * self.__ray_color(scattered, depth-1, world)
            return Color(0, 0, 0)
    
        unit_direction = r.dir.normalize()
        a = (unit_direction.y + 1.0) * 0.5
        return Color(1.0, 1.0, 1.0) * (1.0-a) + Color(0.5, 0.7, 1.0) * a