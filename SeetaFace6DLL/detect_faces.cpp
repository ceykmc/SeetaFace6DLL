#include "detect_faces.h"

// detect face position
void* create_face_detector(const char* p_model_file_path)
{
    seeta::ModelSetting::Device device = seeta::ModelSetting::CPU;
    int id = 0;
    seeta::ModelSetting FD_model(p_model_file_path, device, id);

    return (void*)new seeta::FaceDetector(FD_model);
}

SeetaFaceInfoArray detect_faces(
    void* p_face_detector,
    const SeetaImageData& image)
{
    return ((seeta::FaceDetector*)p_face_detector)->detect(image);
}

void destroy_face_detector(void* p_face_detector)
{
    if (p_face_detector) {
        delete (seeta::FaceDetector*)p_face_detector;
    }
}
