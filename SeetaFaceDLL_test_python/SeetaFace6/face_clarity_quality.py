import ctypes
import os
from typing import Tuple

import numpy as np

from .utility import (SeetaImageData, SeetaPointF, SeetaRect,
                      convert_numpy_array_to_SeetaImageData)


class FaceClarityQuality(object):
    def __init__(self):
        dll_file_path = os.path.join(os.path.dirname(__file__), "lib", "win",
                                     "x64", "SeetaFace6DLL.dll")
        self.dll = ctypes.cdll.LoadLibrary(dll_file_path)
        self.checker = self.create_clarity_quality_checker()

    def create_clarity_quality_checker(self):
        create_clarity_quality_checker = self.dll.create_clarity_quality_checker
        create_clarity_quality_checker.restype = ctypes.c_void_p

        checker = create_clarity_quality_checker()
        return checker

    def destroy_clarity_quality_checker(self):
        destroy_clarity_quality_checker = self.dll.destroy_clarity_quality_checker
        destroy_clarity_quality_checker.argtypes = (ctypes.c_void_p, )
        if self.checker is not None:
            destroy_clarity_quality_checker(self.checker)
            self.checker = None

    def __del__(self):
        self.destroy_clarity_quality_checker()

    def check_clarity_quality(self, image: np.array, face_rect: np.array,
                              face_landmarks: np.array) -> Tuple[int, float]:
        """get face clarity quality level and score

        Parameters
        ----------
        image : np.array
            opencv image, BGR format
        face_rect : np.array
            face rect, shape is 1 x 4, [c_x, c_y, w, h], [0, 1] format
        face_landmarks : np.array
            face landmarks, shape is: 5 x 2, [0, 1] format

        Returns
        -------
        Tuple[int, float] :
            return quality level and quality score
        """
        check_clarity_quality = self.dll.check_clarity_quality
        check_clarity_quality.argtypes = (ctypes.c_void_p,
                                          SeetaImageData, SeetaRect,
                                          ctypes.POINTER(SeetaPointF),
                                          ctypes.POINTER(ctypes.c_int32),
                                          ctypes.POINTER(ctypes.c_float))

        seeta_image = convert_numpy_array_to_SeetaImageData(image)
        c_x, c_y, w, h = face_rect
        x = int((c_x - w / 2) * image.shape[1])
        y = int((c_y - h / 2) * image.shape[0])
        w = int(w * image.shape[1])
        h = int(h * image.shape[0])
        seeta_rect = SeetaRect(x=x, y=y, width=w, height=h)
        assert len(face_landmarks) == 5
        seeta_points = (SeetaPointF * 5)()
        for i in range(5):
            seeta_points[i].x = ctypes.c_double(face_landmarks[i][0] *
                                                image.shape[1])
            seeta_points[i].y = ctypes.c_double(face_landmarks[i][1] *
                                                image.shape[0])

        level = ctypes.c_int(0)
        score = ctypes.c_float(0)
        check_clarity_quality(
            self.checker, seeta_image, seeta_rect,
            ctypes.cast(seeta_points, ctypes.POINTER(SeetaPointF)),
            ctypes.pointer(level), ctypes.pointer(score))

        return level.value, score.value
