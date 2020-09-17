#pragma once

#ifdef _WINDLL
#define DLLEXPORT _declspec(dllexport)
#else
#define DLLEXPORT _declspec(dllimport)
#endif

#include <seeta/FaceLandmarker.h>

#ifdef __cplusplus
extern "C" {
#endif

    DLLEXPORT void* create_landmark_detector(const char* p_model_file_path);

    DLLEXPORT void detect_face_landmarks(
        void* p_landmark_detector,
        const SeetaImageData& image,
        const SeetaRect& face_rect,
        SeetaPointF * points);

    DLLEXPORT void destroy_landmark_detector(void* p_landmark_detector);

#ifdef __cplusplus
}
#endif
