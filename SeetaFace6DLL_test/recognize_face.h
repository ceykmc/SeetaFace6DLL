#pragma once

#ifdef _WINDLL
#define DLLEXPORT _declspec(dllexport)
#else
#define DLLEXPORT _declspec(dllimport)
#endif

#include <seeta/FaceRecognizer.h>

#ifdef __cplusplus
extern "C" {
#endif

    DLLEXPORT void* create_face_recognizer(const char* p_model_file_path);

    DLLEXPORT int get_feature_size(void* p_face_recognizer);

    DLLEXPORT void extract_feature(
        void* p_face_recognizer,
        const SeetaImageData& face_roi_image,
        const SeetaPointF* landmarks,
        float* features);

    DLLEXPORT float computer_similarity(
        void* p_face_recognizer,
        const float* features1,
        const float* features2);

    DLLEXPORT void destroy_face_recognizer(void* p_recognizer);

#ifdef __cplusplus
}
#endif
#pragma once
