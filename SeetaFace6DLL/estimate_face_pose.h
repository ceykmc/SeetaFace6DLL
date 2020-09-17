#pragma once

#ifdef _WINDLL
#define DLLEXPORT _declspec(dllexport)
#else
#define DLLEXPORT _declspec(dllimport)
#endif

#include <seeta/PoseEstimator.h>

#ifdef __cplusplus
extern "C" {
#endif

    DLLEXPORT void* create_face_pose_estimator(const char* p_model_file_path);

    DLLEXPORT void estimate_face_pose(
        void* p_face_pose_estimator,
        const SeetaImageData& image,
        const SeetaRect& face_rect,
        float* yaw,
        float* pitch,
        float* roll);

    DLLEXPORT void destroy_face_pose_estimator(void* p_face_pose_estimator);

#ifdef __cplusplus
}
#endif
