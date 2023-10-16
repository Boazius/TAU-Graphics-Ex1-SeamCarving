from typing import Any, Dict

import numpy as np

NDArray = Any


def resize(image: NDArray, out_height: int, out_width: int) -> Dict[str, NDArray]:
    """
    :param image: ِnp.array which represents an image.
    :param out_height: the resized image height
    :param out_width:  the resized image width
    :return: a dictionary with single element {'resized': img}
        where img is the resized image with the desired dimensions.
    """
    
    # Calculate scaling factors
    sy = image.shape[0] / out_height
    sx = image.shape[1] / out_width
    
    # Determine output shape based on the number of dimensions in the image
    out_shape = (out_height, out_width) if image.ndim == 2 else (out_height, out_width, 3)
    
    # Initialize an output array of zeros with the same data type as the input image
    output = np.zeros(out_shape, dtype=image.dtype)
    
    # Iterate through each pixel of the output image and assign the corresponding pixel from the input image
    for i in range(out_height):
        for j in range(out_width):
            output[i, j, ...] = image[int(sy * i), int(sx * j), ...]
            
    # Return a dictionary with the resized image as the value
    return {'resized': output}
