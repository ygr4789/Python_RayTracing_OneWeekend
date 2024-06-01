import numpy as np
from PIL import Image
from vec3 import Vec3, Point3, Color
from ray import Ray

def ray_color(r: Ray) -> Color:
    if hit_sphere(Point3(0,0,-1), 0.5, r):
        return Color(1, 0, 0)
    
    unit_direction = r.dir.normalize()
    a = (unit_direction.y + 1.0) * 0.5
    return Color(1.0, 1.0, 1.0) * (1.0-a) + Color(0.5, 0.7, 1.0) * a

def write_color(arr: list, c: Color) -> None:
    r = int(255.999 * c.x)
    g = int(255.999 * c.y)
    b = int(255.999 * c.z)
    arr.extend([r, g, b])

def hit_sphere(center: Point3, radius: float, r: Ray) -> bool:
    oc = center - r.orig
    a = r.dir.dot(r.dir)
    b = -2.0 * r.dir.dot(oc)
    c = oc.dot(oc) - radius*radius
    discriminant = b*b - 4*a*c
    return (discriminant >= 0)

def main():
    aspect_ratio = 16.0 / 9.0

    # Calculate the image height
    image_width = int(400)
    image_height = int(image_width / aspect_ratio)

    # Camera
    focal_length = 1.0
    viewport_height = 2.0
    viewport_width = viewport_height * (image_width/image_height)
    camera_center = Point3(0, 0, 0)

    # Calculate the vectors across the horizontal and down the vertical viewport edges.
    viewport_u = Vec3(viewport_width, 0, 0)
    viewport_v = Vec3(0, -viewport_height, 0)

    # Calculate the horizontal and vertical delta vectors from pixel to pixel.
    pixel_delta_u = viewport_u / image_width
    pixel_delta_v = viewport_v / image_height

    # Calculate the location of the upper left pixel.
    viewport_upper_left = camera_center - Vec3(0, 0, focal_length) - viewport_u/2 - viewport_v/2
    pixel00_loc = viewport_upper_left + (pixel_delta_u + pixel_delta_v) * 0.5
    
    color_array: list[float] = []
    
    for v in range(image_height):
        for u in range(image_width):
            pixel_center = pixel00_loc + (pixel_delta_u * u) + (pixel_delta_v * v)
            ray_direction = pixel_center - camera_center
            r = Ray(camera_center, ray_direction)
            
            pixel_color = ray_color(r)
            write_color(color_array, pixel_color)
            
    assert len(color_array) == image_width * image_height * 3
    numpy_array = np.array(color_array, dtype=np.uint8)
    numpy_array = numpy_array.reshape((image_height, image_width, 3))
    image = Image.fromarray(numpy_array)

    image.save("out.png")

if __name__ == "__main__":
    main()