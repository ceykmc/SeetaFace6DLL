import ctypes
import os

import numpy as np

from .utility import (SeetaImageData, SeetaRect,
                      convert_numpy_array_to_SeetaImageData)


class FacePoseEstimation(object):
    def __init__(self):
        dll_file_path = os.path.join(os.path.dirname(__file__), "lib", "win",
                                     "x64", "SeetaFace6DLL.dll")
        model_file_path = os.path.join(os.path.dirname(__file__), "models",
                                       "pose_estimation.csta")
        self.dll = ctypes.cdll.LoadLibrary(dll_file_path)
        self.face_pose_estimator = self.create_face_pose_estimator(model_file_path)

    def create_face_pose_estimator(self, model_file_path):
        create_face_pose_estimator = self.dll.create_face_pose_estimator
        create_face_pose_estimator.argtypes = (ctypes.c_char_p, )
        create_face_pose_estimator.restype = ctypes.c_void_p

        model_file_path = model_file_path.encode("utf-8")
        face_pose_estimator = create_face_pose_estimator(
            ctypes.c_char_p(model_file_path))
        return face_pose_estimator

    def destroy_face_pose_estimator(self):
        destroy_face_pose_estimator = self.dll.destroy_face_pose_estimator
        destroy_face_pose_estimator.argtypes = (ctypes.c_void_p, )
        if self.face_pose_estimator is not None:
            destroy_face_pose_estimator(self.face_pose_estimator)
            self.face_pose_estimator = None

    def __del__(self):
        self.destroy_face_pose_estimator()

    def estimate_face_pose(self, image: np.array, face_rect: np.array):
        estimate_face_pose = self.dll.estimate_face_pose
        estimate_face_pose.argtypes = (ctypes.c_void_p,
                                       SeetaImageData, SeetaRect,
                                       ctypes.POINTER(ctypes.c_float),
                                       ctypes.POINTER(ctypes.c_float),
                                       ctypes.POINTER(ctypes.c_float))
        seeta_image = convert_numpy_array_to_SeetaImageData(image)
        c_x, c_y, w, h = face_rect
        x = int((c_x - w / 2) * image.shape[1])
        y = int((c_y - h / 2) * image.shape[0])
        w = int(w * image.shape[1])
        h = int(h * image.shape[0])
        seeta_rect = SeetaRect(x=x, y=y, width=w, height=h)
        yaw = ctypes.c_float(0)
        pitch = ctypes.c_float(0)
        roll = ctypes.c_float(0)
        estimate_face_pose(self.face_pose_estimator, seeta_image, seeta_rect,
                           ctypes.pointer(yaw), ctypes.pointer(pitch),
                           ctypes.pointer(roll))
        return yaw.value, pitch.value, roll.value
