import numpy as np
from PIL import Image

from hittable_list import *
from sphere import *
from camera import *
from material import *

def main():
    color_array: list[float] = []

    material_ground = Lambertian(Color(0.8, 0.8, 0.0))
    material_center = Lambertian(Color(0.1, 0.2, 0.5))
    material_left = Dielectric(1.5)
    material_bubble = Dielectric(1 / 1.5)
    material_right = Metal(Color(0.8, 0.6, 0.2), 1.0)

    world = HittableList()
    world.add(Sphere(Point3(  0.0, -100.5, -1.0), 100, material_ground))
    world.add(Sphere(Point3(  0.0,    0.0, -1.2), 0.5, material_center))
    world.add(Sphere(Point3( -1.0,    0.0, -1.0), 0.5, material_left))
    world.add(Sphere(Point3( -1.0,    0.0, -1.0), 0.4, material_bubble))
    world.add(Sphere(Point3(  1.0,    0.0, -1.0), 0.5, material_right))

    # cam = Camera(16.0 / 9.0, 100, 20, 10)
    cam = Camera(16.0 / 9.0, 400, 100, 50)
    cam.render(world, color_array)
            
    numpy_array = np.array(color_array, dtype=np.uint8)
    numpy_array = numpy_array.reshape((-1, cam.image_width, 3))
    image = Image.fromarray(numpy_array)

    image.show()
    image.save("out.png")

if __name__ == "__main__":
    main()