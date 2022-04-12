from typing import Dict, Any

import numpy as np
import utils

NDArray = Any


def markSeams(grayImage, seamMatMask, gradientMat, forward_implementation, originalColMat, k):
    """
    :param gradientMat: E(i,j) for each cell. ReadOnly
    :param grayImage: the image in grayscale. ReadOnly
    :param seamMatMask: Write/Read
    :param forward_implementation: boolean, cost matrix calculation method
    :param originalColMat: for each cell saves which column it was before we shrunk it.
    :param k: how many seams to make
    :return: This function marks True and False on verticalSeamMatMask, where the seams are.
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
        mask = np.ones((height, width), dtype=np.bool)

        # Find the position of the smallest element in the last row of M
        j = np.argmin(costMatrix[-1])

        for i in reversed(range(height)):
            # Mark the pixels for deletion
            mask[i, j] = False
            seamMatMask[i, currOriginalColMat[i, j]] = False
            j += backTrackMat[i, j] - 1

        # TODO: shrink grayImage,gradientMat,originalColMat according to mask.
        #  img = np.reshape(image[mask], (r, c - 1))
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
    widthDiff = out_width - width
    heightDiff = out_height - height

    # initialize useful matrices - MAYBE MAKE THIS GLOBAL?

    # saves the image converted to grayscale, WILL BE SHRANK AND ENLARGED
    grayscaleMat = utils.to_grayscale(image)
    gradientMat = utils.get_gradients(grayscaleMat)

    # save for each cell its original row and column.
    _, originalColMat = np.indices((height, width))
    originalRowMat, _ = np.indices((height, out_width))

    # every cell will be TRUE or FALSE, coloured in RED or not this will be in original height and width:
    verticalSeamMatMask = np.ones_like(grayscaleMat, dtype=bool)
    # every cell will be TRUE or FALSE, coloured in Black or not, original height, changed Width
    horizontalSeamMatMask = np.ones((height, out_width), dtype=bool)

    # TODO Output dictionary will have resized image,red line vertical seams image , black line horizontal image
    outDict = {}
    # outResizedImage = np.copy(image)
    # outImageWithVerticalSeams
    # outImageWithHorizontalSeams

    # Mark seams will update verticalSeamMatMask, will not change grayscaleMat, gradientMat, originalColMat
    if heightDiff != 0:
        markSeams(grayscaleMat, verticalSeamMatMask, gradientMat,
                  forward_implementation, originalColMat, np.abs(heightDiff))

        # TODO: create outImageWithVerticalSeams = copy(image) with red seams.

        if heightDiff > 0:
            # TODO: enlarge image, by duplicating all marked cells in verticalSeamMatMask
            #  create a new matrix with 1 or 2. 2 means duplicate cell.
            #  use np.reshape(np.repeat(image,newMask.flatten()),(height,out_width)) . FIX FOR IMAGE RGB
            pass
        if heightDiff < 0:
            # TODO: shrink image by masking all marked cells in verticalSeamMatMask

            # np.reshape(image[:,:,0][verticalSeamMatMask],(height,out_width))
            image[:, :, 0] = np.reshape(image[:, :, 0][verticalSeamMatMask], (height, out_width))

    # TODO rotate the image RGB three dimensions. something with image[:,:,0],image[:,:,1],image[:,:,2] maybe?
    image = rotate_image_counter_clockwise(image)
    # calculate new gradient and grayscale for the image
    grayscaleMat = utils.to_grayscale(image)
    gradientMat = utils.get_gradients(grayscaleMat)

    # TODO: do it again with horizontalSeamMatMask
    if widthDiff != 0:
        markSeams(grayscaleMat, horizontalSeamMatMask, gradientMat,
                  forward_implementation, originalRowMat, np.abs(widthDiff))
        if widthDiff > 0:
            pass  # TODO
        if widthDiff < 0:
            pass  # TODO

    # TODO: return { 'resized' : img1, 'vertical_seams' : img2 ,'horizontal_seams' : img3}
    return outDict


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
        #  faster performance instead of doing minimum twice.
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

    # TODO calculate cv,cr,and cl using np.add, np.roll, np.subtract, np.abs
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
# TODO: handle the grayscale case and the image RGB case.
def rotate_image_clockwise(image: NDArray):
    return np.rot90(image, -1, (0, 1))


# function to rotate image 90 degrees counter clockwise
# TODO: handle the grayscale case and the image RGB case.
def rotate_image_counter_clockwise(image: NDArray):
    return np.rot90(image, 3, (0, 1))
