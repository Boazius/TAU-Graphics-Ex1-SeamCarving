# Authors - Boaz Yakubov and Noga Kinor,
# 323274100 and 311335046

from typing import Dict, Any

import numpy as np
import utils

NDArray = Any

# from PIL import Image
# from matplotlib import pyplot as plt

# def showImage(image):
#     im = Image.fromarray(np.uint8(image))
#     im.show()
#
#
# def showMask(mask):
#     binary = mask > 0
#     plt.imshow(binary)
#     plt.show()


# This function marks True and False on verticalSeamMatMask, where the seams are.
def markSeams(grayImage, seamMatMask, gradientMat, forward_implementation, originalColMat, k):
    """
    :param gradientMat: E(i,j) for each cell. ReadOnly
    :param grayImage: the image in grayscale. ReadOnly
    :param seamMatMask: Write/Read
    :param forward_implementation: boolean, cost matrix calculation method
    :param originalColMat: for each cell saves which column it was before we shrunk it.
    :param k: how many seams to make
    """
    # make copies of the matrices to not modify them, because we don't know if enlarge/shrink
    currGrayImage = np.copy(grayImage)
    currGradientMat = np.copy(gradientMat)
    currOriginalColMat = np.copy(originalColMat)

    # delete and Mark k seams
    for seamIdx in range(k):
        # get cost matrix
        height, width = currGrayImage.shape
        costMatrix, backTrackMat = getCostMatrix(currGrayImage, currGradientMat, forward_implementation)

        # for deleting seam, mark ONLY the seam on the matrix with False.
        mask = np.ones((height, width), dtype=bool)

        # Find the position of the smallest element in the last row of M
        j = np.argmin(costMatrix[-1])

        for i in reversed(range(height)):
            # Mark the pixels for deletion
            mask[i, j] = False
            seamMatMask[i, currOriginalColMat[i, j]] = False
            j += backTrackMat[i, j] - 1

        currGrayImage = np.reshape(currGrayImage[mask], (height, width - 1))
        currGradientMat = np.reshape(currGradientMat[mask], (height, width - 1))
        currOriginalColMat = np.reshape(currOriginalColMat[mask], (height, width - 1))


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
    heightDiff = out_height - height
    widthDiff = out_width - width

    # saves the image converted to grayscale, WILL BE SHRANK AND ENLARGED
    grayscaleMat = utils.to_grayscale(image)
    gradientMat = utils.get_gradients(grayscaleMat)

    # save for each cell its original row and column.
    _, originalColMat = np.indices((height, width))
    # for the rotated image, we will need something like this:
    _, originalRowMat = np.indices((out_width, height))
    # every cell will be TRUE or FALSE, coloured in RED or not this will be in original height and width:
    verticalSeamMatMask = np.ones_like(grayscaleMat, dtype=bool)
    # every cell will be TRUE or FALSE, coloured in Black or not, original height, changed Width
    horizontalSeamMatMask = np.ones((out_width, height), dtype=bool)

    # @@@@@@@@@@@@@@@@@@@@@@  VERTICAL SEAMS  @@@@@@@@@@@@@@@@@@@@@@
    # Mark seams will update verticalSeamMatMask, will not change grayscaleMat, gradientMat, originalColMat
    outImageWithVerticalSeams = np.copy(image)

    if widthDiff != 0:
        # Mark all seams on Matrix mask
        markSeams(grayscaleMat, verticalSeamMatMask, gradientMat,
                  forward_implementation, originalColMat, np.abs(widthDiff))
        # add red lines to image rgb
        outImageWithVerticalSeams[:, :, 0] = np.where(verticalSeamMatMask, outImageWithVerticalSeams[:, :, 0], 255)
        outImageWithVerticalSeams[:, :, 1] = np.where(verticalSeamMatMask, outImageWithVerticalSeams[:, :, 1], 0)
        outImageWithVerticalSeams[:, :, 2] = np.where(verticalSeamMatMask, outImageWithVerticalSeams[:, :, 2], 0)

        if widthDiff > 0:
            # enlarge image
            repeatMat = np.invert(verticalSeamMatMask) + 1
            image = np.dstack((np.reshape(np.repeat(image[:, :, 0], repeatMat.flatten()), (height, out_width)),
                               np.reshape(np.repeat(image[:, :, 1], repeatMat.flatten()), (height, out_width)),
                               np.reshape(np.repeat(image[:, :, 2], repeatMat.flatten()), (height, out_width))))
            # showImage(newImage)

        if widthDiff < 0:
            # shrink image
            image = np.dstack((np.reshape(image[:, :, 0][verticalSeamMatMask], (height, out_width)),
                               np.reshape(image[:, :, 1][verticalSeamMatMask], (height, out_width)),
                               np.reshape(image[:, :, 2][verticalSeamMatMask], (height, out_width))))
            # showImage(newImage)



    # @@@@@@@@@@@@@@@@@@@@@@  Horizontal SEAMS  @@@@@@@@@@@@@@@@@@@@@@
    # Mark seams will update horizontalSeamMatMask, will not change grayscaleMat, gradientMat, originalColMat
    outImageWithHorizontalSeams = np.copy(image)

    if heightDiff != 0:
        # rotate the image RGB
        image = rotate_image_counter_clockwise(image)
        # calculate new gradient and grayscale for the image - easier than rotating and reshaping
        grayscaleMat = utils.to_grayscale(image)
        gradientMat = utils.get_gradients(grayscaleMat)
        # showImage(image)
        # Mark all seams on Matrix mask
        markSeams(grayscaleMat, horizontalSeamMatMask, gradientMat,
                  forward_implementation, originalRowMat, np.abs(heightDiff))
        # add black lines to image rgb
        outImageWithHorizontalSeams[:, :, 0] = np.where(horizontalSeamMatMask, outImageWithHorizontalSeams[:, :, 0], 0)
        outImageWithHorizontalSeams[:, :, 1] = np.where(horizontalSeamMatMask, outImageWithHorizontalSeams[:, :, 1], 0)
        outImageWithHorizontalSeams[:, :, 2] = np.where(horizontalSeamMatMask, outImageWithHorizontalSeams[:, :, 2], 0)
        outImageWithHorizontalSeams = rotate_image_clockwise(outImageWithHorizontalSeams)
        # showImage(outImageWithHorizontalSeams)

        if heightDiff > 0:
            # enlarge image - notice we switched width and height , because its rotated!
            repeatMat = np.invert(horizontalSeamMatMask) + 1
            image = np.dstack(
                (np.reshape(np.repeat(image[:, :, 0], repeatMat.flatten()), (out_width, out_height)),
                 np.reshape(np.repeat(image[:, :, 1], repeatMat.flatten()), (out_width, out_height)),
                 np.reshape(np.repeat(image[:, :, 2], repeatMat.flatten()), (out_width, out_height))))
            # image = rotate_image_clockwise(image)
            # showImage(image)

        if heightDiff < 0:
            # shrink image  - notice we switched width and height , because its rotated!
            image = np.dstack((np.reshape(image[:, :, 0][horizontalSeamMatMask], (out_width, out_height)),
                               np.reshape(image[:, :, 1][horizontalSeamMatMask], (out_width, out_height)),
                               np.reshape(image[:, :, 2][horizontalSeamMatMask], (out_width, out_height))))
            # image = rotate_image_clockwise(image)
            # showImage(image)

        image = rotate_image_clockwise(image)

    return {'resized': image, 'vertical_seams': outImageWithVerticalSeams,
            'horizontal_seams': outImageWithHorizontalSeams}


def getCostMatrix(grayscaleMat: NDArray, gradientMat: NDArray, forward_implementation: bool) -> (NDArray, NDArray):
    """

    :param gradientMat: Energy for each i,j
    :param grayscaleMat: a matrix of the image, in grayscale.
    :param forward_implementation: the calculation is different depending on the implementation
    :return: the completed cost matrix, and the backtracking matrix
            backTrackingMat: for every cell, the value is either 0 1 or 2:
            1 for upper left cell, 2 for upper cell, 3 for upper right cell
            denotes the cell that gave the current cell its value (in the cost matrix.
    """
    # get E(i,j).
    height, width = grayscaleMat.shape

    # calculate forward energy if needed (or just zeroes)
    if forward_implementation:
        # create three forward energy matrices for cl, cv, and cr
        forwardCL, forwardCV, forwardCR = get_forward_energy_matrix(grayscaleMat, width)
    else:
        # just zeroes
        forwardCR = forwardCV = forwardCL = np.zeros_like(grayscaleMat)

    # find cost matrix using gradients and forward energy by going row by row and getting minimums from prev row
    costMatrix = np.copy(gradientMat)
    backTrackingMat = np.zeros_like(grayscaleMat, dtype=int)

    # for every row calculate cost matrix using the previous row.
    for i in range(1, height):
        # M[i-1,j-1]
        costRollUpLeft = np.roll(costMatrix[i - 1], shift=1)
        # M[i-1,j] is costMatrix[i - 1]
        # M[i-1,j+1]
        costRollUpRight = np.roll(costMatrix[i - 1], shift=-1)
        # arrange the candidates in a list
        possibleValueForCostMatrixRow = [np.add(costRollUpLeft, forwardCL[i]), np.add(costMatrix[i - 1], forwardCV[i]),
                                         np.add(costRollUpRight, forwardCR[i])]
        # find the minimum index (0 1 or 2 meaning left, up, or right ), and copy the value into costMatrix
        backTrackingMat[i] = np.argmin(possibleValueForCostMatrixRow, axis=0)
        # TODO: use the indexes from backTrackingMat to somehow select the correct values from three different arrays,
        #  faster performance instead of doing minimum twice. THIS SLOWS IT DOWN SIGNIFICANTLY
        np.add(costMatrix[i], np.min(possibleValueForCostMatrixRow, axis=0), out=costMatrix[i])

        # edge cases - left edge j=0, right edge j = width-1
        possibleValLeftEdge = [costMatrix[i - 1, 0] + forwardCV[i, 0], costRollUpRight[0] + forwardCR[i, 0]]
        backTrackingMat[i, 0] = np.argmin(possibleValLeftEdge) + 1  # because it cant be 0 (left)
        costMatrix[i, 0] = gradientMat[i, 0] + np.min(possibleValLeftEdge)
        possibleValRightEdge = [costMatrix[i - 1, width - 1] + forwardCV[i, width - 1],
                                costRollUpRight[width - 1] + forwardCR[i, width - 1]]
        backTrackingMat[i, width - 1] = np.argmin(possibleValRightEdge)
        costMatrix[i, width - 1] = gradientMat[i, width - 1] + np.min(possibleValRightEdge)

    return costMatrix, backTrackingMat


# this function calculates Cv, Cr, and Cl for a given grayscale image
def get_forward_energy_matrix(grayScaleMat: NDArray, width) -> \
        (NDArray, NDArray, NDArray):
    forwardCV = np.empty_like(grayScaleMat)
    forwardCL = np.empty_like(grayScaleMat)
    forwardCR = np.empty_like(grayScaleMat)

    # calculate cv,cr,and cl using np.add, np.roll, np.subtract, np.abs
    matRollJPlus1 = np.roll(grayScaleMat, axis=1, shift=-1)  # take j+1
    matRollJMinus1 = np.roll(grayScaleMat, axis=1, shift=1)  # take j-1
    matRollIMinus1 = np.roll(grayScaleMat, axis=0, shift=1)  # take i-1

    # CV
    np.copyto(forwardCV, matRollJPlus1)
    np.subtract(forwardCV, matRollJMinus1, out=forwardCV)
    np.absolute(forwardCV, out=forwardCV)
    # CL
    np.copyto(forwardCL, matRollIMinus1)
    np.subtract(forwardCL, matRollJMinus1, out=forwardCL)
    np.absolute(forwardCL, out=forwardCL)
    np.add(forwardCL, forwardCV, out=forwardCL)
    # CR
    np.copyto(forwardCR, matRollIMinus1)
    np.subtract(forwardCR, matRollJPlus1, out=forwardCR)
    np.absolute(forwardCR, out=forwardCR)
    np.add(forwardCR, forwardCV, out=forwardCR)

    # calculate left and right edges
    # CR = absolute ( I(i,1) - I(i-1,0) )
    np.copyto(forwardCR[:, 0], grayScaleMat[:, 1])
    np.subtract(forwardCR[:, 0], np.roll(grayScaleMat[:, 0], axis=0, shift=1), out=forwardCR[:, 0])
    np.absolute(forwardCR[:, 0], out=forwardCR[:, 0])

    # CL = absolute ( I(i-1,width) - I(i,width-1) )
    np.copyto(forwardCL[:, width - 1], grayScaleMat[:, width - 2])
    np.subtract(forwardCL[:, width - 1], np.roll(grayScaleMat[:, width - 1], axis=0, shift=1),
                out=forwardCL[:, width - 1])
    np.absolute(forwardCL[:, width - 1], out=forwardCL[:, width - 1])

    # add 255 to CL,CV,CR on the edges.
    forwardCL[:, width - 1] += 255
    forwardCV[:, width - 1] += 255
    forwardCV[:, 0] += 255
    forwardCR[:, 0] += 255

    return forwardCL, forwardCV, forwardCR


# function to rotate image 90 degrees clockwise
def rotate_image_counter_clockwise(image: NDArray):
    return np.rot90(image, -1, (1, 0))


# function to rotate image 90 degrees counter clockwise
def rotate_image_clockwise(image: NDArray):
    return np.rot90(image, 3, (0, 1))
