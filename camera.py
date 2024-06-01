from hittable import *

def _write_color(target: list, c: Color) -> None:
    r = int(255.999 * c.x)
    g = int(255.999 * c.y)
    b = int(255.999 * c.z)
    target.extend([r, g, b])

class Camera:
    def __init__(self, aspect_ratio:float = 1.0, image_width:int = 100) -> None:
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
        
        self.__image_height: int
        self.__center: Point3
        self.__pixel_delta_u: float
        self.__pixel_delta_v: float
        self.__pixel00_loc: Point3
    
    def render(self, world:Hittable, target:list) -> None:
        self.__initialize()
        
        for v in range(self.__image_height):
            for u in range(self.image_width):
                pixel_center = self.__pixel00_loc + (self.__pixel_delta_u * u) + (self.__pixel_delta_v * v)
                ray_direction = pixel_center - self.__center
                r = Ray(self.__center, ray_direction)
                
                pixel_color = self.__ray_color(r, world)
                _write_color(target, pixel_color)
    
    def __initialize(self) -> None:
        image_width = self.image_width
        image_height = int(image_width / self.aspect_ratio)
        
        focal_length = 1.0
        viewport_height = 2.0
        viewport_width = viewport_height * (image_width/image_height)
        center = Point3(0, 0, 0)

        viewport_u = Vec3(viewport_width, 0, 0)
        viewport_v = Vec3(0, -viewport_height, 0)

        pixel_delta_u = viewport_u / image_width
        pixel_delta_v = viewport_v / image_height

        viewport_upper_left = center - Vec3(0, 0, focal_length) - viewport_u/2 - viewport_v/2
        pixel00_loc = viewport_upper_left + (pixel_delta_u + pixel_delta_v) * 0.5
        
        self.__image_height = image_height
        self.__center = center
        self.__pixel_delta_u = pixel_delta_u
        self.__pixel_delta_v = pixel_delta_v
        self.__pixel00_loc = pixel00_loc
    
    def __ray_color(self, r:Ray, world:Hittable) -> Color:
        # Convert normal to color
        if rec := world.hit(r, Interval(0, math.inf)):
            return (rec.normal + Color(1,1,1)) * 0.5
    
        # Default background
        unit_direction = r.dir.normalize()
        a = (unit_direction.y + 1.0) * 0.5
        return Color(1.0, 1.0, 1.0) * (1.0-a) + Color(0.5, 0.7, 1.0) * a