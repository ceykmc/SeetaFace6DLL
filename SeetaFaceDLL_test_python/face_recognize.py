import cv2
import ctypes

import convert
import SeetaFace_data_struct


def extract_landmarks(image_path):
    cv_image = cv2.imread(image_path)
    seeta_image = convert.convert_numpy_array_to_SeetaImageData(cv_image)

    dll_file_path = "../x64/Release/SeetaFace6DLL.dll"
    dll = ctypes.cdll.LoadLibrary(dll_file_path)

    create_landmark_detector = dll.create_landmark_detector
    create_landmark_detector.argtypes = (ctypes.c_char_p, )
    create_landmark_detector.restype = ctypes.c_void_p

    detect_face_landmarks = dll.detect_face_landmarks
    detect_face_landmarks.argtypes = (ctypes.c_void_p,
                                      SeetaFace_data_struct.SeetaImageData,
                                      SeetaFace_data_struct.SeetaRect,
                                      ctypes.POINTER(
                                          SeetaFace_data_struct.SeetaPointF))
    destroy_landmark_detector = dll.destroy_landmark_detector
    destroy_landmark_detector.argtypes = (ctypes.c_void_p, )

    landmark_model_file_path = "./SeetaFaceSDK/models/face_landmarker_pts5.csta"
    landmark_model_file_path = landmark_model_file_path.encode("utf-8")
    landmark_detector = create_landmark_detector(
        ctypes.c_char_p(landmark_model_file_path))

    seeta_rect = SeetaFace_data_struct.SeetaRect(x=0,
                                                 y=0,
                                                 width=cv_image.shape[1],
                                                 height=cv_image.shape[0])
    points = (SeetaFace_data_struct.SeetaPointF * 5)()
    detect_face_landmarks(
        landmark_detector, seeta_image, seeta_rect,
        ctypes.cast(points, ctypes.POINTER(SeetaFace_data_struct.SeetaPointF)))
    destroy_landmark_detector(landmark_detector)

    return points


def test_face_recognize(image_path_a, image_path_b):
    points_a = extract_landmarks(image_path_a)
    points_b = extract_landmarks(image_path_b)

    cv_image_a = cv2.imread(image_path_a)
    seeta_image_a = convert.convert_numpy_array_to_SeetaImageData(cv_image_a)
    cv_image_b = cv2.imread(image_path_b)
    seeta_image_b = convert.convert_numpy_array_to_SeetaImageData(cv_image_b)

    dll_file_path = "../x64/Release/SeetaFace6DLL.dll"
    dll = ctypes.cdll.LoadLibrary(dll_file_path)

    # create
    create_face_recognizer = dll.create_face_recognizer
    create_face_recognizer.argtypes = (ctypes.c_char_p, )
    create_face_recognizer.restype = ctypes.c_void_p

    get_feature_size = dll.get_feature_size
    get_feature_size.argtypes = (ctypes.c_void_p, )
    get_feature_size.restype = ctypes.c_int

    extract_feature = dll.extract_feature
    extract_feature.argtypes = (ctypes.c_void_p,
                                SeetaFace_data_struct.SeetaImageData,
                                ctypes.POINTER(
                                    SeetaFace_data_struct.SeetaPointF),
                                ctypes.POINTER(ctypes.c_float))

    computer_similarity = dll.computer_similarity
    computer_similarity.argtypes = (ctypes.c_void_p,
                                    ctypes.POINTER(ctypes.c_float),
                                    ctypes.POINTER(ctypes.c_float))
    computer_similarity.restype = ctypes.c_float

    destroy_face_recognizer = dll.destroy_face_recognizer
    destroy_face_recognizer.argtypes = (ctypes.c_void_p, )

    # process
    model_file_path = "./SeetaFaceSDK/models/face_recognizer.csta"
    model_file_path = model_file_path.encode("utf-8")
    recognizer = create_face_recognizer(model_file_path)

    feature_size = get_feature_size(recognizer)
    feature_a = (ctypes.c_float * feature_size)()
    feature_b = (ctypes.c_float * feature_size)()
    extract_feature(
        recognizer, seeta_image_a,
        ctypes.cast(points_a,
                    ctypes.POINTER(SeetaFace_data_struct.SeetaPointF)),
        ctypes.cast(feature_a, ctypes.POINTER(ctypes.c_float)))
    extract_feature(
        recognizer, seeta_image_b,
        ctypes.cast(points_b,
                    ctypes.POINTER(SeetaFace_data_struct.SeetaPointF)),
        ctypes.cast(feature_b, ctypes.POINTER(ctypes.c_float)))

    similarity = computer_similarity(
        recognizer, ctypes.cast(feature_a, ctypes.POINTER(ctypes.c_float)),
        ctypes.cast(feature_b, ctypes.POINTER(ctypes.c_float)))

    print(F"similarity: {similarity}, {type(similarity)}")
    destroy_face_recognizer(recognizer)


def main():
    image_path_a = "./data/126-1060-309-152-111_1_.png"
    image_path_b = "./data/133-1672-0-84-90_0_.png"
    test_face_recognize(image_path_a, image_path_b)


if __name__ == "__main__":
    main()
