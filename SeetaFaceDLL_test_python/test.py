import ctypes

import cv2
import SeetaFace_data_struct
import convert


def main():
    # prepare data
    image_path = "./data/126-1060-309-152-111_1_.png"
    cv_image = cv2.imread(image_path)

    img_h = ctypes.c_int32(cv_image.shape[0])
    img_w = ctypes.c_int32(cv_image.shape[1])
    img_c = ctypes.c_int32(cv_image.shape[2])

    rect = (ctypes.c_int32 * 4)()
    rect[0], rect[1], rect[2], rect[3] = \
        ctypes.c_int32(0), ctypes.c_int32(0), img_w, img_h

    points = (ctypes.c_double * 10)()
    points[0], points[1] = ctypes.c_double(33.8604), ctypes.c_double(50.8867)
    points[2], points[3] = ctypes.c_double(70.4262), ctypes.c_double(56.923)
    points[4], points[5] = ctypes.c_double(44.2245), ctypes.c_double(74.5922)
    points[6], points[7] = ctypes.c_double(39.8662), ctypes.c_double(88.8391)
    points[8], points[9] = ctypes.c_double(68.6998), ctypes.c_double(92.397)

    level = ctypes.c_int32(0)
    score = ctypes.c_float(0)

    # load dll
    dll_file_path = "../x64/Release/SeetaFace6DLL.dll"
    dll = ctypes.cdll.LoadLibrary(dll_file_path)

    # clarity quality check
    create_clarity_quality_checker = dll.create_clarity_quality_checker
    create_clarity_quality_checker.restype = ctypes.c_void_p

    destroy_clarity_quality_checker = dll.destroy_clarity_quality_checker
    destroy_clarity_quality_checker.argtypes = (ctypes.c_void_p, )

    check_clarity_quality = dll.check_clarity_quality
    check_clarity_quality.argtypes = (ctypes.c_void_p, ctypes.c_int32,
                                      ctypes.c_int32, ctypes.c_int32,
                                      ctypes.POINTER(ctypes.c_uint8),
                                      ctypes.c_int32 * 4, ctypes.c_double * 10,
                                      ctypes.POINTER(ctypes.c_int32),
                                      ctypes.POINTER(ctypes.c_float))

    clarity_quality_checker = create_clarity_quality_checker()
    check_clarity_quality(
        clarity_quality_checker, img_h, img_w, img_c,
        cv_image.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)), rect, points,
        ctypes.pointer(level), ctypes.pointer(score))
    destroy_clarity_quality_checker(clarity_quality_checker)
    print(F"clarity quality level: {level}, score: {score}")

    # pose quality check
    create_pose_quality_checker = dll.create_pose_quality_checker
    create_pose_quality_checker.restype = ctypes.c_void_p

    destroy_pose_quality_checker = dll.destroy_pose_quality_checker
    destroy_pose_quality_checker.argtypes = (ctypes.c_void_p, )

    check_pose_quality = dll.check_pose_quality
    check_pose_quality.argtypes = (ctypes.c_void_p, ctypes.c_int32,
                                   ctypes.c_int32, ctypes.c_int32,
                                   ctypes.POINTER(ctypes.c_uint8),
                                   ctypes.c_int32 * 4, ctypes.c_double * 10,
                                   ctypes.POINTER(ctypes.c_int32),
                                   ctypes.POINTER(ctypes.c_float))

    pose_quality_checker = create_pose_quality_checker()
    check_pose_quality(pose_quality_checker, img_h, img_w, img_c,
                       cv_image.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),
                       rect, points, ctypes.pointer(level),
                       ctypes.pointer(score))
    destroy_pose_quality_checker(pose_quality_checker)
    print(F"pose quality level: {level}, score: {score}")

    # pose estimation
    create_face_pose_estimator = dll.create_face_pose_estimator
    create_face_pose_estimator.argtypes = (ctypes.c_char_p, )
    create_face_pose_estimator.restype = ctypes.c_void_p

    destroy_face_pose_estimator = dll.destroy_face_pose_estimator
    destroy_face_pose_estimator.argtypes = (ctypes.c_void_p, )

    estimate_face_pose = dll.estimate_face_pose
    estimate_face_pose.argtypes = (
        ctypes.c_void_p,
        SeetaFace_data_struct.SeetaImageData,
        SeetaFace_data_struct.SeetaRect,
        ctypes.POINTER(ctypes.c_float),
        ctypes.POINTER(ctypes.c_float),
        ctypes.POINTER(ctypes.c_float)
    )

    yaw = ctypes.c_float(0)
    pitch = ctypes.c_float(0)
    roll = ctypes.c_float(0)
    pose_model_file_path = "./SeetaFaceSDK/models/pose_estimation.csta"
    seeta_image = convert.convert_numpy_array_to_SeetaImageData(cv_image)
    seeta_rect = SeetaFace_data_struct.SeetaRect(x=0, y=0, width=112, height=112)
    pose_model_file_path = pose_model_file_path.encode("utf-8")
    face_pose_estimator = create_face_pose_estimator(
        ctypes.c_char_p(pose_model_file_path))
    print("------ start ------")
    estimate_face_pose(face_pose_estimator,
                       seeta_image,
                       seeta_rect,
                       ctypes.pointer(yaw),
                       ctypes.pointer(pitch),
                       ctypes.pointer(roll))
    print("------ end ------")
    destroy_face_pose_estimator(face_pose_estimator)
    print(F"face angles, yaw: {yaw}, pitch: {pitch}, roll: {roll}")


if __name__ == "__main__":
    main()
