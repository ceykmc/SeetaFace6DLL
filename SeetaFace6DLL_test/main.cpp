#include <iostream>
#include <opencv2/opencv.hpp>
#include "detect_face_landmarks.h"
#include "recognize_face.h"

void test_landmark()
{
    const char* model_file_path = "./SeetaFaceSDK/models/face_landmarker_pts5.csta";
    void* landmark_detector = create_landmark_detector(model_file_path);

    const char* image_path = "./data/126-1060-309-152-111_1_.png";
    cv::Mat image = cv::imread(image_path);
    SeetaImageData seeta_image = { int(image.cols), int(image.rows), int(image.channels()), image.data };
    SeetaRect seeta_rect = { 0, 0, int(image.cols), int(image.rows) };
    std::vector<SeetaPointF> points(5);
    detect_face_landmarks(landmark_detector, seeta_image, seeta_rect, points.data());

    for (size_t i = 0; i < points.size(); ++i) {
        int x = int(points[i].x);
        int y = int(points[i].y);
        cv::circle(image, cv::Point(x, y), 3, cv::Scalar(0, 255, 0), -1);
    }
    cv::imshow("landmarks", image);
    cv::waitKey();
    cv::destroyAllWindows();

    destroy_landmark_detector(landmark_detector);
}

void test_recognize()
{
    const char* landmark_model_file_path = "./SeetaFaceSDK/models/face_landmarker_pts5.csta";
    void* landmark_detector = create_landmark_detector(landmark_model_file_path);
    const char* recognize_model_file_path = "./SeetaFaceSDK/models/face_recognizer.csta";
    void* recognizer = create_face_recognizer(recognize_model_file_path);

    const char* image_path_a = "./data/126-1060-309-152-111_1_.png";
    cv::Mat image_a = cv::imread(image_path_a);
    SeetaImageData seeta_image_a = {
        int(image_a.cols), int(image_a.rows), int(image_a.channels()), image_a.data 
    };
    SeetaRect seeta_rect_a = { 0, 0, int(image_a.cols), int(image_a.rows) };
    std::vector<SeetaPointF> points_a(5);
    detect_face_landmarks(landmark_detector, seeta_image_a, seeta_rect_a, points_a.data());

    const char* image_path_b = "./data/133-1672-0-84-90_0_.png";
    cv::Mat image_b = cv::imread(image_path_b);
    SeetaImageData seeta_image_b = {
        int(image_b.cols), int(image_b.rows), int(image_b.channels()), image_b.data 
    };
    SeetaRect seeta_rect_b = { 0, 0, int(image_b.cols), int(image_b.rows) };
    std::vector<SeetaPointF> points_b(5);
    detect_face_landmarks(landmark_detector, seeta_image_b, seeta_rect_b, points_b.data());

    int feature_size = get_feature_size(recognizer);
    std::vector<float> feature_a(feature_size), feature_b(feature_size);
    extract_feature(recognizer, seeta_image_a, points_a.data(), feature_a.data());
    extract_feature(recognizer, seeta_image_b, points_b.data(), feature_b.data());
    float similarity = computer_similarity(recognizer, feature_a.data(), feature_b.data());
    std::cout << "similarity is: " << similarity << std::endl;

    destroy_landmark_detector(landmark_detector);
    destroy_face_recognizer(recognizer);
}

int main()
{
    test_recognize();
    system("pause");
    return 0;
}
