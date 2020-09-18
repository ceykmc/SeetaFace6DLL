import cv2

from SeetaFace6 import FaceDetector, FaceRecognizer, LandmarkDetector


def extract_image_feature(image_path):
    face_detector = FaceDetector()
    landmark_detector = LandmarkDetector()
    face_recognizer = FaceRecognizer()

    image = cv2.imread(image_path)
    faces = face_detector.detect_faces(image)
    face_rect = faces[0][:4].tolist()
    points = landmark_detector.detect_face_landmarks(image, face_rect)
    features = face_recognizer.extract_feature(image, points)
    return features


def main():
    image_path_a = "./data/128-1820-66-108-102_0_.png"
    image_path_b = "./data/wtp.png"
    feature_a = extract_image_feature(image_path_a)
    feature_b = extract_image_feature(image_path_b)

    face_recognizer = FaceRecognizer()
    similarity = face_recognizer.computer_similarity(feature_a, feature_b)
    print(F"similarity is: {similarity:.2f}")


if __name__ == "__main__":
    main()
