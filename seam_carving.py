from typing import Dict, Any

import utils

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

    # TODO convert image to grayscale

    # width = image.getWidth();
    # height = image.getHeight();
    # widthDiff = out_width - width;
    # heightDiff = out_height - height;

    # if heightDiff > 0: # we need to enlarge height
    # TODO add heightDiff seams

    # if heightDiff < 0 # we need to shrink height
    # TODO remove heightDiff seams

    # if widthDiff > 0 # rotate and do the same
    # TODO Rotate image, add widthDiff Seams

    # if widthDiff <0 #rotate and do the same
    # TODO Rotate image, remove widthDiff seams

    # costMatrix = get_cost_matrix(image,forward_implementation)

    # TODO: figure out if we calculate cost matrix each time we delete/add a seam, or calculate once and use it for
    #  all seams

    # TODO:
    #  for 1 to k:
    #   Use dynamic programming to find the optimal vertical seam using the cost matrix
    #   Find the actual seam by finding the smallest cost in the bottom row, then start going up on a path using the backtracking matrix
    #   Remove the seam from the grayscale image - DO NOT create a new image (inefficient) , just mark them as removed somehow.
    #   Store the order and pixels removed in each iteration - will be used for the red and black lines

    # To reduce image size by 𝑘 pixels, remove all chosen seams from the original image
    # To enlarge by 𝑘 pixels, duplicate all chosen seams from the original image.

    # TODO: return { 'resized' : img1, 'vertical_seams' : img2 ,'horizontal_seams' : img3}

    # TODO  when adding seams, we must find all k best seams using the same cost matrix, and only then
    #  duplicate them all once.


    # TODO, also keep for each pixel its original (in the original image) (i,j) index in a different matrix.



def remove_k_seams(image: NDArray, out_height: int, out_width: int, forward_implementation: bool, k:int):
    # TODO this function removes the best seam from the image, k times.
    #  when deleting seams, we must delete one by one: i.e, calculate cost matrix, delete the seam, and calculate
    #  cost matrix again....
    pass


def get_cost_matrix(image: NDArray, forward_implementation: bool):
    """

    :param image:
    :param forward_implementation: the calculation is different depending on the implementation
    :return: an array
    """

    # if the forward implementation is true, just add the C_L or C_V or C_R.
    # if its false M C_L and C_V and C_R is zero.

    # TODO compute the image gradient function E using get_gradients(image: NDArray):
    # gradientMatrix = utils.get_gradients(image)

    # TODO this function must also create the backtracking matrix
    #  to figure out which pixel gave the current pixel its valu
    #
    # TODO when calculating cost matrix, also create a matrix for backtracking the best seam: when calculating a cost
    #  for a pixel, save in this new matrix if we used the (i-1,j-1) or (i-1,j) or (i,j-1) pixel for the cost
    #  calculatiion. so when we go up the matrix, we use this new backtracking matrix to decide on the seam path.
    pass


def rotate_image_clockwise(image: NDArray, out_height: int, out_width: int):
    pass
    # TODO function to rotate image  90 degrees counter clockwise or clockwise- use numpy rotate


def rotate_image_counter_clockwise(image: NDArray, out_height: int, out_width: int):
    pass
    # TODO function to rotate image  90 degrees counter clockwise or clockwise- use numpy rotate

