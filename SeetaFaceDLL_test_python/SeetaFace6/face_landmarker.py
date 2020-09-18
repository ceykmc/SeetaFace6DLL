import ctypes
import os

import numpy as np

from .utility import (SeetaImageData, SeetaPointF, SeetaRect,
                      convert_numpy_array_to_SeetaImageData)


class LandmarkDetector(object):
    def __init__(self):
        dll_file_path = os.path.join(os.path.dirname(__file__), "lib", "win",
                                     "x64", "SeetaFace6DLL.dll")
        model_file_path = os.path.join(os.path.dirname(__file__), "models",
                                       "face_landmarker_pts5.csta")
        self.dll = ctypes.cdll.LoadLibrary(dll_file_path)
        self.landmark_detector = self.create_landmark_detector(model_file_path)

    def create_landmark_detector(self, model_file_path):
        create_landmark_detector = self.dll.create_landmark_detector
        create_landmark_detector.argtypes = (ctypes.c_char_p, )
        create_landmark_detector.restype = ctypes.c_void_p

        model_file_path = model_file_path.encode("utf-8")
        landmark_detector = create_landmark_detector(
            ctypes.c_char_p(model_file_path))
        return landmark_detector

    def destroy_landmark_detector(self):
        destroy_landmark_detector = self.dll.destroy_landmark_detector
        destroy_landmark_detector.argtypes = (ctypes.c_void_p, )
        if self.landmark_detector is not None:
            destroy_landmark_detector(self.landmark_detector)
            self.landmark_detector = None

    def __del__(self):
        self.destroy_landmark_detector()

    def detect_face_landmarks(self, image: np.array, face_rect: np.array):
        detect_face_landmarks = self.dll.detect_face_landmarks
        detect_face_landmarks.argtypes = (ctypes.c_void_p,
                                          SeetaImageData, SeetaRect,
                                          ctypes.POINTER(SeetaPointF))

        seeta_image = convert_numpy_array_to_SeetaImageData(image)
        c_x, c_y, w, h = face_rect
        x = int((c_x - w / 2) * image.shape[1])
        y = int((c_y - h / 2) * image.shape[0])
        w = int(w * image.shape[1])
        h = int(h * image.shape[0])
        face_rect = SeetaRect(x=x, y=y, width=w, height=h)

        seeta_points = (SeetaPointF * 5)()
        detect_face_landmarks(
            self.landmark_detector, seeta_image, face_rect,
            ctypes.cast(seeta_points, ctypes.POINTER(SeetaPointF)))
        points = np.zeros(shape=[5, 2], dtype=np.float32)
        for i in range(5):
            x = seeta_points[i].x / image.shape[1]
            y = seeta_points[i].y / image.shape[0]
            points[i, :] = [x, y]
        return points
