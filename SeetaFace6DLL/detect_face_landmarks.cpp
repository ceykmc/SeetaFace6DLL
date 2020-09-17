#include "detect_face_landmarks.h"

void* create_landmark_detector(const char* p_model_file_path)
{
    seeta::ModelSetting::Device device = seeta::ModelSetting::CPU;
    int id = 0;
    seeta::ModelSetting FD_model(p_model_file_path, device, id);

    return (void*)new seeta::FaceLandmarker(FD_model);
}

void detect_face_landmarks(
    void* p_landmark_detector,
    const SeetaImageData& image,
    const SeetaRect& face_rect,
    SeetaPointF* points)
{
    ((seeta::FaceLandmarker*)p_landmark_detector)->mark(image, face_rect, points);
}

void destroy_landmark_detector(void* p_landmark_detector)
{
    if (p_landmark_detector) {
        delete (seeta::FaceLandmarker*)p_landmark_detector;
    }
}
