#pragma once

#ifdef _WINDLL
#define DLLEXPORT _declspec(dllexport)
#else
#define DLLEXPORT _declspec(dllimport)
#endif

#include <seeta/FaceDetector.h>

#ifdef __cplusplus
extern "C" {
#endif

    DLLEXPORT void* create_face_detector(const char* p_model_file_path);

    DLLEXPORT SeetaFaceInfoArray detect_faces(
        void* p_face_detector,
        const SeetaImageData& image);

    DLLEXPORT void destroy_face_detector(void* p_face_detector);

#ifdef __cplusplus
}
#endif
