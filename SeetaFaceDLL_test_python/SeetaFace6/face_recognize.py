import ctypes
import os

import numpy as np

from .utility import (SeetaImageData, SeetaPointF,
                      convert_numpy_array_to_SeetaImageData)


class FaceRecognizer(object):
    def __init__(self):
        dll_file_path = os.path.join(os.path.dirname(__file__), "lib", "win",
                                     "x64", "SeetaFace6DLL.dll")
        model_file_path = os.path.join(os.path.dirname(__file__), "models",
                                       "face_recognizer.csta")
        self.dll = ctypes.cdll.LoadLibrary(dll_file_path)
        self.face_recognizer = self.create_face_recognizer(model_file_path)

    def create_face_recognizer(self, model_file_path):
        create_face_recognizer = self.dll.create_face_recognizer
        create_face_recognizer.argtypes = (ctypes.c_char_p, )
        create_face_recognizer.restype = ctypes.c_void_p

        model_file_path = model_file_path.encode("utf-8")
        face_recognizer = create_face_recognizer(
            ctypes.c_char_p(model_file_path))
        return face_recognizer

    def destroy_face_recognizer(self):
        destroy_face_recognizer = self.dll.destroy_face_recognizer
        destroy_face_recognizer.argtypes = (ctypes.c_void_p, )
        if self.face_recognizer is not None:
            destroy_face_recognizer(self.face_recognizer)
            self.face_recognizer = None

    def __del__(self):
        self.destroy_face_recognizer()

    def get_feature_size(self) -> int:
        get_feature_size = self.dll.get_feature_size
        get_feature_size.argtypes = (ctypes.c_void_p, )
        get_feature_size.restype = ctypes.c_int
        feature_size = get_feature_size(self.face_recognizer)
        return feature_size

    def extract_feature(self, image: np.array,
                        face_landmarks: np.array) -> np.array:
        extract_feature = self.dll.extract_feature
        extract_feature.argtypes = (ctypes.c_void_p, SeetaImageData,
                                    ctypes.POINTER(SeetaPointF),
                                    ctypes.POINTER(ctypes.c_float))

        seeta_image = convert_numpy_array_to_SeetaImageData(image)
        seeta_points = (SeetaPointF * 5)()
        for i in range(5):
            seeta_points[i].x = ctypes.c_double(face_landmarks[i][0] *
                                                image.shape[1])
            seeta_points[i].y = ctypes.c_double(face_landmarks[i][1] *
                                                image.shape[0])
        feature_size = self.get_feature_size()
        seeta_feature = (ctypes.c_float * feature_size)()
        extract_feature(
            self.face_recognizer, seeta_image,
            ctypes.cast(seeta_points, ctypes.POINTER(SeetaPointF)),
            ctypes.cast(seeta_feature, ctypes.POINTER(ctypes.c_float)))
        feature = np.ctypeslib.as_array(seeta_feature)
        return feature

    def computer_similarity(self, feature_a: np.array,
                            feature_b: np.array) -> float:
        computer_similarity = self.dll.computer_similarity
        computer_similarity.argtypes = (ctypes.c_void_p,
                                        ctypes.POINTER(ctypes.c_float),
                                        ctypes.POINTER(ctypes.c_float))
        computer_similarity.restype = ctypes.c_float

        similarity = computer_similarity(
            self.face_recognizer,
            feature_a.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            feature_b.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))
        return similarity
