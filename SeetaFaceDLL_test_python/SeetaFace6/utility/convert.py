import ctypes
from typing import List

import numpy as np

from .SeetaFace_data_struct import SeetaImageData, SeetaRect


def convert_numpy_array_to_SeetaImageData(image_np: np.ndarray):
    seeta_image = SeetaImageData()
    seeta_image.width = ctypes.c_int32(image_np.shape[1])
    seeta_image.height = ctypes.c_int32(image_np.shape[0])
    seeta_image.channels = ctypes.c_int32(image_np.shape[2])
    seeta_image.data = image_np.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
    return seeta_image


def convert_list_to_SeetaRect(rect: List[int]):
    seeta_rect = SeetaRect()
    seeta_rect.x = ctypes.c_int(rect[0])
    seeta_rect.y = ctypes.c_int(rect[1])
    seeta_rect.width = ctypes.c_int(rect[2])
    seeta_rect.height = ctypes.c_int(rect[3])
    return seeta_rect
