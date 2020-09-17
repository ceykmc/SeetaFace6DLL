#include "recognize_face.h"

void* create_face_recognizer(const char* p_model_file_path)
{
    seeta::ModelSetting::Device device = seeta::ModelSetting::CPU;
    int id = 0;
    seeta::ModelSetting FD_model(p_model_file_path, device, id);

    return (void*)new seeta::FaceRecognizer(FD_model);
}

void destroy_face_recognizer(void* p_recognizer)
{
    delete (seeta::FaceRecognizer*)p_recognizer;
}

int get_feature_size(void* p_face_recognizer)
{
    return ((seeta::FaceRecognizer*)p_face_recognizer)->GetExtractFeatureSize();
}

void extract_feature(
    void* p_face_recognizer,
    const SeetaImageData& face_roi_image,
    const SeetaPointF* landmarks,
    float* features)
{
    ((seeta::FaceRecognizer*)p_face_recognizer)->Extract(face_roi_image, landmarks, features);
}

float computer_similarity(
    void* p_face_recognizer,
    const float* features1,
    const float* features2)
{
    return ((seeta::FaceRecognizer*)p_face_recognizer)->CalculateSimilarity(features1, features2);
}
