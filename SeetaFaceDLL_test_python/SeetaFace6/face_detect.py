import ctypes
import os

import cv2
import numpy as np

from .utility import (SeetaFaceInfoArray, SeetaImageData,
                      convert_numpy_array_to_SeetaImageData)


class FaceDetector(object):
    def __init__(self):
        dll_file_path = os.path.join(os.path.dirname(__file__), "lib", "win",
                                     "x64", "SeetaFace6DLL.dll")
        model_file_path = os.path.join(os.path.dirname(__file__), "models",
                                       "face_detector.csta")
        self.dll = ctypes.cdll.LoadLibrary(dll_file_path)
        self.face_detector = self.create_face_detector(model_file_path)

    def create_face_detector(self, model_file_path):
        create_face_detector = self.dll.create_face_detector
        create_face_detector.argtypes = (ctypes.c_char_p, )
        create_face_detector.restype = ctypes.c_void_p

        model_file_path = model_file_path.encode("utf-8")
        face_detector = create_face_detector(ctypes.c_char_p(model_file_path))
        return face_detector

    def destroy_face_detector(self):
        destroy_face_detector = self.dll.destroy_face_detector
        destroy_face_detector.argtypes = (ctypes.c_void_p, )
        if self.face_detector is not None:
            destroy_face_detector(self.face_detector)
            self.face_detector = None

    def __del__(self):
        self.destroy_face_detector()

    def detect_faces(self, image):
        detect_faces = self.dll.detect_faces
        detect_faces.argtypes = (
            ctypes.c_void_p,
            SeetaImageData,
        )
        detect_faces.restype = SeetaFaceInfoArray

        seeta_image = convert_numpy_array_to_SeetaImageData(image)

        faces = np.array([], dtype=np.float32)
        if self.face_detector:
            seeta_faces = detect_faces(self.face_detector, seeta_image)
            if seeta_faces.size > 0:
                faces = np.zeros(shape=[seeta_faces.size, 5], dtype=np.float32)
                for i in range(seeta_faces.size):
                    x1 = seeta_faces.data[i].pos.x / image.shape[1]
                    y1 = seeta_faces.data[i].pos.y / image.shape[0]
                    w = seeta_faces.data[i].pos.width / image.shape[1]
                    h = seeta_faces.data[i].pos.height / image.shape[0]
                    score = seeta_faces.data[i].score
                    faces[i] = [x1 + w / 2, y1 + h / 2, w, h, score]
        return faces
