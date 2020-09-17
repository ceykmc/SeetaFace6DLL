#include <iostream>
#include <opencv2/opencv.hpp>
#include "detect_face_landmarks.h"

void test_landmark()
{
    const char* model_file_path = "./SeetaFaceSDK/models/face_landmarker_pts5.csta";
    void* landmark_detector = create_landmark_detector(model_file_path);

    //seeta::ModelSetting::Device device = seeta::ModelSetting::CPU;
    //int id = 0;
    //std::string landmark_model = "./SeetaFaceSDK/models/face_landmarker_pts5.csta";
    //seeta::ModelSetting landmark_setting(landmark_model, device, id);
    //seeta::FaceLandmarker* m_landmark = new seeta::FaceLandmarker(landmark_setting);

    const char* image_path = "./data/126-1060-309-152-111_1_.png";
    cv::Mat image = cv::imread(image_path);
    std::cout << image.size() << std::endl;
    SeetaImageData seeta_image = { int(image.cols), int(image.rows), int(image.channels()), image.data };
    SeetaRect seeta_rect = { 0, 0, int(image.cols), int(image.rows) };
    std::vector<SeetaPointF> points(5);
    detect_face_landmarks(landmark_detector, seeta_image, seeta_rect, points.data());
    //std::vector<SeetaPointF> points = m_landmark->mark(seeta_image, seeta_rect);

    for (size_t i = 0; i < points.size(); ++i) {
        std::cout << points[i].x << " " << points[i].y << std::endl;
    }

    //if (m_landmark) {
    //    delete m_landmark;
    //    m_landmark = nullptr;
    //}

    destroy_landmark_detector(landmark_detector);
}

int main()
{
    test_landmark();
    system("pause");
    return 0;
}
