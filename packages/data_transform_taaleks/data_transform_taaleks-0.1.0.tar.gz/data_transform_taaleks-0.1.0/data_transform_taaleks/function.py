import numpy as np


def transpose_multi_d(input_matrix: list[list[float]]) -> list[list[float]]:
    """
    Function takes any kind list of lists, transpose it.
    NOTE: All lists in the list must contain the same number of items.

    Args:
        input_matrix (list[list[float]]): matrix

    Returns:
        list: tranposed list of lists
    """
    # Test input_matrix
    if not isinstance(input_matrix, list):
        return 'ValueError: input_matrix needs to be a list'

    if not isinstance(input_matrix[0], list):
        return 'ValueError: input_matrix needs to be a list of lists'

    list_len = len(input_matrix[0])
    for matrix_list in input_matrix:
        if len(matrix_list) != list_len:
            return 'ValueError: all lists in input_matrix must be the same length'

    # Main logic
    if len(input_matrix) == 1:
        trans_list = input_matrix
    else:
        trans_list = [list(item) for item in [list(row)
                                              for row in zip(*input_matrix)]]
    return trans_list


def window1d(input_array: list | np.ndarray, size: int, shift: int = 1, stride: int = 1) -> list[list | np.ndarray]:
    """
    Generates sliding windows from a 1D array or list with specified size, shift, and stride.

    Args:
        input_array (list | np.ndarray): A list or 1D NumPy array of real numbers from which to generate windows.
        size (int): The size (length) of each window.
        shift (int, optional): The shift (step size) between the starting points of consecutive windows. Defaults to 1.
        stride (int, optional): The stride (step size) within each window. Defaults to 1.

    Returns:
        list[list | np.ndarray]: A list of lists or 1D NumPy arrays, each representing a window of the specified size.
    """
    # Test input_array
    if not isinstance(input_array, list):
        if not isinstance(input_array, np.array):
            return 'ValueError: input_array must be either a list or np.array'

    for item in input_array:
        if not isinstance(item, (int, float)):
            return f'ValueError: input_array must contains real numbers. {type(item)} datatype was provided'

    # Test size
    if not isinstance(size, int):
        return f'ValueError: size must be integer. {type(size)} datatype was provided'

    if size < 1:
        return f'ValueError: size must be positive integer. {size} was provided'

    if size > len(input_array):
        return f'ValueError: size cannot be larger than the length of the input array'

    # Test shift
    if not isinstance(shift, int):
        return f'ValueError: shift must be integer. {type(shift)} datatype was provided'

    if shift < 1:
        return f'ValueError: shift must be positive integer. {shift} was provided'

    # Test stride
    if not isinstance(stride, int):
        return f'ValueError: shift must be integer. {type(stride)} datatype was provided'

    if stride < 1:
        return f'ValueError: shift must be positive integer. {stride} was provided'

    # Main logic
    if isinstance(input_array, list):
        input_array = np.array(input_array)

    window_list = []

    for start in range(0, len(input_array) - size + 1, shift):
        window = input_array[start:start + size:stride]
        window_list.append(window.tolist() if isinstance(
            window, np.ndarray) else window)

    return window_list


def convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1) -> np.ndarray:
    """
    Apply a 2D convolution operation to the input matrix using the given kernel and stride.

    Args:
        input_matrix (np.ndarray): 2D array representing the input matrix.
        kernel (np.ndarray): 2D array representing the convolution kernel.
        stride (int, optional): The stride of the convolution. Must be greater than 0. Default is 1.

    Returns:
        np.ndarray: 2D array representing the result of the convolution operation.
    """

    # Test input_matrix
    if not isinstance(input_matrix, np.ndarray):
        return f'ValueError: input_matrix must be np.ndarray. {type(input_matrix)} was provided'

    for row in input_matrix:
        for column in row:
            if not isinstance(column, np.int64):
                return f'ValueError: all values in input_matrix must be real numbers'

    # Test kernel
    if not isinstance(kernel, np.ndarray):
        return f'ValueError: input_matrix must be np.ndarray. {type(kernel)} was provided'

    for row in kernel:
        for column in row:
            if not isinstance(column, np.int64):
                return f'ValueError: all values in input_matrix must be real numbers'

    # Test stride
    if not isinstance(stride, int):
        return f'ValueError: stride must be integer. {type(stride)} was provided'

    if stride < 1:
        return f'ValueError: stride must be higher than 0'

    input_height, input_width = input_matrix.shape
    kernel_height, kernel_width = kernel.shape

    output_height = (input_height - kernel_height) // stride + 1
    output_width = (input_width - kernel_width) // stride + 1

    output_matrix = np.zeros((output_height, output_width))

    for i in range(0, output_height):
        for j in range(0, output_width):
            sub_matrix = input_matrix[i*stride:i*stride +
                                      kernel_height, j*stride:j*stride+kernel_width]
            output_matrix[i, j] = np.sum(sub_matrix * kernel)
    return output_matrix
