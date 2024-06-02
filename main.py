import random
import numpy as np
from PIL import Image

from hittable_list import *
from sphere import *
from camera import *
from material import *

def main():
    color_array: list[float] = []

    world = HittableList()

    ground_material = Lambertian(Color(0.5, 0.5, 0.5))
    world.add(Sphere(Point3(0,-1000,0), 1000, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random.random()
            center = Point3(a + 0.9*random.random(), 0.2, b + 0.9*random.random())

            if center.distance(Point3(4, 0.2, 0)) > 0.9:
                if choose_mat < 0.8:
                    albedo = Color.random() * Color.random()
                    sphere_material = Lambertian(albedo)
                    world.add(Sphere(center, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    albedo = Color.random(0.5, 1)
                    fuzz = random.uniform(0, 0.5)
                    sphere_material = Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                else:
                    sphere_material = Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))

    material1 = Dielectric(1.5)
    world.add(Sphere(Point3(0, 1, 0), 1.0, material1))

    material2 = Lambertian(Color(0.4, 0.2, 0.1))
    world.add(Sphere(Point3(-4, 1, 0), 1.0, material2))

    material3 = Metal(Color(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(Point3(4, 1, 0), 1.0, material3))

    cam = Camera()

    cam.aspect_ratio      = 16.0 / 9.0
    cam.image_width       = 400
    cam.samples_per_pixel = 100
    cam.max_depth         = 50

    cam.vfov     = 20
    cam.lookfrom = Point3(13,2,3)
    cam.lookat   = Point3(0,0,0)
    cam.vup      = Vec3(0,1,0)

    cam.defocus_angle = 0.6
    cam.focus_dist    = 10.0
    
    cam.render(world, color_array)
            
    numpy_array = np.array(color_array, dtype=np.uint8)
    numpy_array = numpy_array.reshape((-1, cam.image_width, 3))
    image = Image.fromarray(numpy_array)

    image.show()
    image.save("out.png")

if __name__ == "__main__":
    main()