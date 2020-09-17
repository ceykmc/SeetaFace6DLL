import ctypes

import cv2

import convert
import SeetaFace_data_struct


def main():
    # prepare data
    image_path = "./data/cgl.png"
    cv_image = cv2.imread(image_path)
    seeta_image = convert.convert_numpy_array_to_SeetaImageData(cv_image)

    model_file_path = "./SeetaFaceSDK/models/face_detector.csta"
    model_file_path = model_file_path.encode("utf-8")

    # load dll
    dll_file_path = "../x64/Release/SeetaFace6DLL.dll"
    dll = ctypes.cdll.LoadLibrary(dll_file_path)

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

    face_detector = create_face_detector(ctypes.c_char_p(model_file_path))
    faces = detect_faces(face_detector, seeta_image)
    destroy_face_detector(face_detector)

    for i in range(faces.size):
        face_info = faces.data[i]
        x1 = face_info.pos.x
        y1 = face_info.pos.y
        x2 = face_info.pos.x + face_info.pos.width - 1
        y2 = face_info.pos.x + face_info.pos.height - 1
        score = face_info.score
        print(F"face {i + 1} score is: {score:.2f}")
        cv2.rectangle(cv_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv2.imshow("faces", cv_image)
    cv2.waitKey()


if __name__ == "__main__":
    main()
