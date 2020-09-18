import cv2

from SeetaFace6 import FaceDetector, LandmarkDetector


def main():
    face_detector = FaceDetector()
    landmark_detector = LandmarkDetector()

    image_path = "./data/cgl.png"
    image = cv2.imread(image_path)
    faces = face_detector.detect_faces(image)

    face_rect = faces[0][:4].tolist()
    points = landmark_detector.detect_face_landmarks(image, face_rect)

    for face in faces:
        c_x, c_y, w, h = face[:4]
        x1 = int((c_x - w / 2) * image.shape[1])
        y1 = int((c_x - h / 2) * image.shape[0])
        x2 = int((c_x + w / 2) * image.shape[1])
        y2 = int((c_x + h / 2) * image.shape[0])
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 255), 2)
    for point in points:
        x = int((point[0] * image.shape[1]))
        y = int((point[1] * image.shape[0]))
        cv2.circle(image, (x, y), 3, (0, 0, 255), -1)
    cv2.imshow("faces", image)
    cv2.waitKey()


if __name__ == "__main__":
    main()
