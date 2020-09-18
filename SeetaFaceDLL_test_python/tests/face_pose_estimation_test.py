import cv2

from SeetaFace6 import FaceDetector, FacePoseEstimation


def main():
    face_detector = FaceDetector()
    face_pose_estimator = FacePoseEstimation()

    image_path = "./data/cgl.png"
    image = cv2.imread(image_path)
    faces = face_detector.detect_faces(image)

    yaw, pitch, roll = face_pose_estimator.estimate_face_pose(
        image, faces[0][:4])
    print(F"face angles: {yaw}, {pitch}, {roll}")
    for face in faces:
        c_x, c_y, w, h = face[:4]
        x1 = int((c_x - w / 2) * image.shape[1])
        y1 = int((c_x - h / 2) * image.shape[0])
        x2 = int((c_x + w / 2) * image.shape[1])
        y2 = int((c_x + h / 2) * image.shape[0])
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 255), 2)
    cv2.imshow("faces", image)
    cv2.waitKey()


if __name__ == "__main__":
    main()
