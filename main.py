import numpy as np
from PIL import Image

from hittable_list import *
from sphere import *
from camera import *

def main():
    color_array: list[float] = []

    world = HittableList()
    world.add(Sphere(Point3(0,0,-1), 0.5))
    world.add(Sphere(Point3(0,-100.5,-1), 100))

    cam = Camera(16.0 / 9.0, 400, 100)
    cam.render(world, color_array)
            
    numpy_array = np.array(color_array, dtype=np.uint8)
    numpy_array = numpy_array.reshape((-1, cam.image_width, 3))
    image = Image.fromarray(numpy_array)

    image.show()
    image.save("out.png")

if __name__ == "__main__":
    main()