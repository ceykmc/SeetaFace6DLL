import ctypes

import cv2

import convert
import SeetaFace_data_struct


def copy_faces(origin_faces):
    faces = SeetaFace_data_struct.SeetaFaceInfoArray()
    faces.size = origin_faces.size
    faces.data = (SeetaFace_data_struct.SeetaFaceInfo * origin_faces.size)()
    for i in range(faces.size):
        faces.data[i] = origin_faces.data[i]
    # faces.data = ctypes.cast(faces.data, ctypes.POINTER(SeetaFace_data_struct.SeetaFaceInfo))
    return faces


def main():
    # prepare data
    image_path = "./data/cgl.png"
    cv_image = cv2.imread(image_path)
    seeta_image = convert.convert_numpy_array_to_SeetaImageData(cv_image)

    face_model_file_path = "./SeetaFaceSDK/models/face_detector.csta"
    face_model_file_path = face_model_file_path.encode("utf-8")

    # load dll
    dll_file_path = "../x64/Release/SeetaFace6DLL.dll"
    dll = ctypes.cdll.LoadLibrary(dll_file_path)

    # detect face
    create_face_detector = dll.create_face_detector
    create_face_detector.argtypes = (ctypes.c_char_p, )
    create_face_detector.restype = ctypes.c_void_p

    detect_faces = dll.detect_faces
    detect_faces.argtypes = (
        ctypes.c_void_p,
        SeetaFace_data_struct.SeetaImageData,
    )
    detect_faces.restype = SeetaFace_data_struct.SeetaFaceInfoArray

    destroy_face_detector = dll.destroy_face_detector
    destroy_face_detector.argtypes = (ctypes.c_void_p, )

    face_detector = create_face_detector(ctypes.c_char_p(face_model_file_path))
    faces = detect_faces(face_detector, seeta_image)
    faces = copy_faces(faces)
    destroy_face_detector(face_detector)

    # detect face landmarks
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

    print("------ start ------")
    landmark_model_file_path = "./SeetaFaceSDK/models/face_landmarker_pts5.csta"
    landmark_model_file_path = landmark_model_file_path.encode("utf-8")
    landmark_detector = create_landmark_detector(
        ctypes.c_char_p(landmark_model_file_path))

    face_info = faces.data[0]
    seeta_rect = SeetaFace_data_struct.SeetaRect(x=face_info.pos.x,
                                                 y=face_info.pos.y,
                                                 width=face_info.pos.width,
                                                 height=face_info.pos.height)
    points = (SeetaFace_data_struct.SeetaPointF * 5)()
    detect_face_landmarks(
        landmark_detector, seeta_image, seeta_rect,
        ctypes.cast(points, ctypes.POINTER(SeetaFace_data_struct.SeetaPointF)))
    destroy_landmark_detector(landmark_detector)
    print("------ end ------")

    face_info = faces.data[0]
    x1 = face_info.pos.x
    y1 = face_info.pos.y
    x2 = face_info.pos.x + face_info.pos.width - 1
    y2 = face_info.pos.x + face_info.pos.height - 1
    cv2.rectangle(cv_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    for i in range(5):
        x, y = int(points[i].x), int(points[i].y)
        cv2.circle(cv_image, (x, y), 3, (0, 255, 0), -1)
    cv2.imshow("faces", cv_image)
    cv2.waitKey()


if __name__ == "__main__":
    main()
