import numpy as np
from PIL import Image
from vec3 import Vec3, Point3, Color

def main():
    image_width = 256
    image_height = 256
    
    color_array: list[list[list[float]]] = []
    
    for i in range(image_height):
        color_array.append([])
        for j in range(image_width):
            pixel_color = Color(j / (image_width-1), i / (image_height-1), 0)
            color_array[i].append(pixel_color.byte())
            
    numpy_array = np.array(color_array, dtype=np.uint8)
    image = Image.fromarray(numpy_array)

    image.save("out.png")

if __name__ == "__main__":
    main()