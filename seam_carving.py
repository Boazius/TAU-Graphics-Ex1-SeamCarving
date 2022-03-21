from typing import Dict, Any

NDArray = Any


def resize(image: NDArray, out_height: int, out_width: int, forward_implementation: bool) -> Dict[str, NDArray]:
    """

    :param image: ِnp.array which represents an image.
    :param out_height: the resized image height
    :param out_width: the resized image width
    :param forward_implementation: a boolean flag that indicates whether forward or basic implementation is used.
                                    if forward_implementation is true then the forward-looking energy is used otherwise
                                    the basic implementation is used.
    :return: A dictionary with three elements, {'resized' : img1, 'vertical_seams' : img2 ,'horizontal_seams' : img3},
            where img1 is the resized image and img2/img3 are the visualization images
            (where the chosen seams are colored red and black for vertical and horizontal seams, respectively).
    """
    raise NotImplementedError('You need to implement this!')
    # TODO: return { 'resized' : img1, 'vertical_seams' : img2 ,'horizontal_seams' : img3}

    # call the correct implementation, depending on forward_implementation

def resize_with_basic_implementation(image: NDArray, out_height: int, out_width: int) -> Dict[str, NDArray]:
    """

    :param image: ِnp.array which represents an image.
    :param out_height: the resized image height
    :param out_width: the resized image width
    :return: A dictionary with three elements, {'resized' : img1, 'vertical_seams' : img2 ,'horizontal_seams' : img3},
            where img1 is the resized image and img2/img3 are the visualization images
            (where the chosen seams are colored red and black for vertical and horizontal seams, respectively)
    """
    # compute the image gradient function E using get_gradients(image: NDArray):

    #for 1 to k:
    #   Use dynamic programming to find the optimal vertical seam by calculating the cost matrix 𝑀.
    #   Find the actual seam by finding the smallest cost in the bottom row, then start going up on a path of minimal costs.
    #   Remove the seam from the grayscale image.
    #   Store the order and pixels removed in each iteration.

    # To reduce image size by 𝑘 pixels, remove all chosen seams from the original image
    # To enlarge by 𝑘 pixels, duplicate all chosen seams from the original image.


def resize_with_forward_implementation(image: NDArray, out_height: int, out_width: int) -> Dict[str, NDArray]:
    """

    :param image: ِnp.array which represents an image.
    :param out_height: the resized image height
    :param out_width: the resized image width
    :return: A dictionary with three elements, {'resized' : img1, 'vertical_seams' : img2 ,'horizontal_seams' : img3},
            where img1 is the resized image and img2/img3 are the visualization images
            (where the chosen seams are colored red and black for vertical and horizontal seams, respectively)
    """



# function to calculate optimal vertical seam with dynamic programing


# function to rotate image  90 degrees counter clockwise

# function to rotate image 90 deg clock wise

#
# Reducing/Increasing the image height by k pixels:
#   To change the size in the height-dimension, you can rotate the image by 90 degrees counter-
#   clockwise and apply the algorithm we outlined above on the rotated image. Once done, you can
#     undo the rotation.