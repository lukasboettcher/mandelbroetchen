import numpy as np
from concurrent.futures import ProcessPoolExecutor
from PIL import Image


def calc_row(row):
    res = np.zeros((1, len(row)))
    for index, z in enumerate(row):
        c = z
        color = 0.
        for i in range(max_iter):
            z = z ** 2 + c
            if abs(z) > 8:
                color = 1.0 - 0.02 * \
                    (i - np.log2(np.log2(z.real*z.real + z.imag * z.imag)))
                break
        res[0, index] = color
    return res


if __name__ == '__main__':
    pixels = 1000
    x_range = (-0.91, -0.76)
    y_range = (-0.3, -0.15)
    # print(abs(x_range[0]- x_range[1]))
    # print(abs(y_range[0]- y_range[1]))
    # assert(abs(x_range[0]- x_range[1]) == abs(y_range[0]- y_range[1]))
    x, y = np.meshgrid(np.linspace(x_range[0], x_range[1], pixels),
                       np.linspace(y_range[0], y_range[1], pixels) * 1j)
    y_indexes = np.arange(pixels)
    max_iter = 255
    result = np.zeros((pixels, pixels))
    with ProcessPoolExecutor() as executor:
        for col, res in enumerate(executor.map(calc_row, x+y)):
            result[col, :] = res
        image = np.clip(result*255, 0, 255).astype(np.uint8)
        image = Image.fromarray(image)
        image.save('out.png')
