from typing import Dict, Any

import utils
import numpy as np
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

    # get width and height, and count how many seams to add/remove horizontally and vertically
    height, width, _ = image.shape
    widthDiff = out_width - width
    heightDiff = out_height - height

    # initialize useful matrices - MAYBE MAKE THIS GLOBAL?

    # saves the image converted to grayscale, WILL BE SHRANK AND ENLARGED
    grayscaleMat = utils.to_grayscale(image)

    # TODO: save for each cell its original row and column, WILL BE SHRANK AND ENLARGED
    originalRowMat, originalColMat = np.indices((height, width))

    # TODO: every cell will be TRUE or FALSE, coloured in RED or not.
    #  this will be in original height and width:
    outputVerticalSeamMat = np.zeros_like(grayscaleMat, dtype=bool)
    # TODO: every cell will be TRUE or FALSE, coloured in Black or not.
    #  this will be in new shrunk/enlarged width (after removing/adding vertical seams),
    #  but in original height (before adding/removing horizontal seams).
    outputHorizontalSeamMat = np.zeros((height, out_width), dtype=bool)

    # TODO: backtracking matrix. for every cell, the value is either 1 2 or 3:
    #  1 for upper left cell, 2 for upper cell, 3 for upper right cell
    #  denotes the cell that gave the current cell its value in the cost matrix.
    currBackTrackingMat = np.zeros_like(grayscaleMat, dtype=int)

    # TODO: cost matrix. WILL BE SHRANK AND ENLARGED. float value here.
    currCostMat = get_cost_matrix(grayscaleMat, currBackTrackingMat, forward_implementation)

    # add or remove k seams horizontally
    if heightDiff > 0:
        resized_image = add_k_seams(image, out_height, out_width, forward_implementation, heightDiff)
    if heightDiff < 0:
        resized_image = remove_k_seams(image, out_height, out_width, forward_implementation, heightDiff)

    # rotate the image, add/remove k seams horizontally, and rotate back
    if widthDiff > 0:
        resized_image = rotate_image_counter_clockwise(
            add_k_seams(rotate_image_clockwise(image, height, out_width),
                        out_height, out_width, forward_implementation, widthDiff))
    if widthDiff < 0:
        resized_image = rotate_image_counter_clockwise(
            remove_k_seams(rotate_image_clockwise(image, height, out_width), out_height, out_width,
                           forward_implementation, widthDiff))

    # TODO: return { 'resized' : img1, 'vertical_seams' : img2 ,'horizontal_seams' : img3}


def remove_k_seams(image: NDArray, out_height: int, out_width: int, forward_implementation: bool, k: int):
    # TODO this function removes the best seam from the image, k times.
    #  when deleting seams, we must delete one by one: i.e, calculate cost matrix, delete the seam, and calculate
    #  cost matrix again....
    currHeight, currWidth = image.shape
    for i in range(k):  # use range if you don't want to use tqdm
        img = carve_column(image)
    return img


def add_k_seams(image: NDArray, out_height: int, out_width: int, forward_implementation: bool, k: int):
    # TODO this function duplicates the best seam from the image, k times.
    # TODO  when adding seams, we must find all k best seams using the same cost matrix, and only then
    #   #  duplicate them all once.
    r, c = image.shape
    for i in range(k):  # use range if you don't want to use tqdm
        img = carve_column(image)
    return img


def carve_column(image: NDArray, forward_implementation: bool):
    r, c = image.shape
    # TODO: will not do grayscale here, we only need to do this once, not for every seam
    gray_image = utils.to_grayscale(image)
    M, backtrack = minimum_seam(gray_image, forward_implementation)

    # Create a (r, c) matrix filled with the value True
    # We'll be removing all pixels from the image which
    # have False later
    mask = np.ones((r, c), dtype=np.bool)

    # Find the position of the smallest element in the
    # last row of M
    j = np.argmin(M[-1])

    for i in reversed(range(r)):
        # Mark the pixels for deletion
        mask[i, j] = False
        j = backtrack[i, j]
    # Delete all the pixels marked False in the mask,
    # and resize it to the new image dimensions
    img = image[mask]
    return img


# image in gray scale
def minimum_seam(image: NDArray, forward_implementation: bool):
    r, c = image.shape
    cost_matrix = get_cost_matrix(image, forward_implementation)
    M = cost_matrix.copy()
    backtrack = np.zeros_like(M, dtype=np.int)

    for i in range(1, r):
        for j in range(0, c):
            # Handle the left edge of the image, to ensure we don't index -1
            if j == 0:
                index = np.argmin(M[i - 1, j:j + 2])
                backtrack[i, j] = index + j
                min_energy = M[i - 1, index + j]
            else:
                index = np.argmin(M[i - 1, j - 1:j + 2])
                backtrack[i, j] = index + j - 1
                min_energy = M[i - 1, index + j - 1]
            M[i, j] += min_energy
    return M, backtrack


def get_cost_matrix(grayScaleMat: NDArray, currBackTrackingMat: NDArray, forward_implementation: bool):
    """

    :param grayScaleMat: a matrix of the image, in grayscale.
    :param currBackTrackingMat: for every cell, the value is either 1 2 or 3:
            1 for upper left cell, 2 for upper cell, 3 for upper right cell
            denotes the cell that gave the current cell its value in the cost matrix.
    :param forward_implementation: the calculation is different depending on the implementation
    :return: the completed cost matrix
    """
    # get E(i,j).
    gradientMatrix = utils.get_gradients(grayScaleMat)
    height, width = grayScaleMat.shape

    # TODO change this to empty_like for faster performance
    costMatrix = np.zeros_like(grayScaleMat)

    # first row is just E(0,j)
    np.copyto(costMatrix[0], grayScaleMat[0])

    # calculate forward energy if needed (or just zeroes)
    if forward_implementation:
        # create three forward energy matrixes for cl, cv, and cr
        forwardCL, forwardCV, forwardCR = get_forward_energy_matrix(grayScaleMat, height, width)
    else:
        # just zeroes
        forwardCR = forwardCV = forwardCL = np.zeros_like(grayScaleMat)

    #  if j=0 (1st col) - ignore M[i-1,j-1] - make it INT_MAX and cl = 255
    #  if j=width (last col) - ignore M[i-1,j+1] - make it INT_MAX and cr = 255

    # TODO: find min(M[i-1,j-1]+cl(i,j), M[i-1,j]+cv(i,j), M[i-1,j+1]+cr(i,j))

    # TODO this function must also create the backtracking matrix
    #  to figure out which pixel gave the current pixel its valu
    #
    # TODO when calculating cost matrix, also create a matrix for backtracking the best seam: when calculating a cost
    #  for a pixel, save in this new matrix if we used the (i-1,j-1) or (i-1,j) or (i,j-1) pixel for the cost
    #  calculations. so when we go up the matrix, we use this new backtracking matrix to decide on the seam path.
    return 0


# this function calculates Cv, Cr, and Cl for a given grayscale image, and its gradient matrix
def get_forward_energy_matrix(grayScaleMat: NDArray, height, width) -> \
        (NDArray, NDArray, NDArray):
    forwardCL = np.zeros_like(grayScaleMat)
    forwardCV = np.zeros_like(grayScaleMat)
    forwardCR = np.zeros_like(grayScaleMat)

    # calculate cv,cr,and cl using np.add, np.roll, np.subtract, np.abs
    tmpRoll = np.roll(grayScaleMat)
    # calculate left and right edges
    # CR = absolute ( I(i,1) - I(i-1,0) )
    np.copyto(forwardCR[:, 0], grayScaleMat[:, 1])
    np.subtract(forwardCR[:, 0], np.roll(grayScaleMat[:, 0], axis=0, shift=1), out=forwardCR[:, 0])
    np.absolute(forwardCR[:, 0], out=forwardCR[:, 0])

    # CL = absolute ( I(i-1,width) - I(i,width-1) )
    np.copyto(forwardCL[:, width-1], grayScaleMat[:, width-2])
    np.subtract(forwardCL[:, width-1], np.roll(grayScaleMat[:, width-1], axis=0, shift=1), out=forwardCL[:, width - 1])
    np.absolute(forwardCL[:, width-1], out=forwardCL[:, width-1])

    # add 255 to CL,CV,CR on the edges.
    forwardCL[:, width - 1] += 255
    forwardCV[:, width - 1] += 255
    forwardCV[:, 0] += 255
    forwardCR[:, 0] += 255

    return forwardCL, forwardCV, forwardCR


# function to rotate image 90 degrees clockwise
# TODO: handle the grayscale case and the image RGB case.
def rotate_image_clockwise(image: NDArray, out_height: int, out_width: int):
    return np.rot90(image, -1, (0, 1))


# function to rotate image 90 degrees counter clockwise
# TODO: handle the grayscale case and the image RGB case.
def rotate_image_counter_clockwise(image: NDArray, out_height: int, out_width: int):
    return np.rot90(image, 3, (0, 1))
