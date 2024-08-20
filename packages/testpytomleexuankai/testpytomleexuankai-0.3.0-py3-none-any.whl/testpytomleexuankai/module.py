import numpy as np

def add_arrays(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Add two numpy arrays element-wise.

    Parameters:
    a (np.ndarray): The first array.
    b (np.ndarray): The second array.

    Returns:
    np.ndarray: The element-wise sum of the two arrays.
    """
    return np.add(a, b)


def add(a: int, b: int):
    "add two numbers"
    return a + b