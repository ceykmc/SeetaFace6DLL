#pragma once

#ifdef _WINDLL
#define DLLEXPORT _declspec(dllexport)
#else
#define DLLEXPORT _declspec(dllimport)
#endif

#ifdef __cplusplus
extern "C" {
#endif

    // clarity quality
    DLLEXPORT void* create_clarity_quality_checker();

    DLLEXPORT void check_clarity_quality(
        void* p_clarity_quality_checker,
        int img_h,
        int img_w,
        int img_c,
        unsigned char* img_data,
        int face_rect[4],
        double face_landmarks[10],
        int* quality_level,
        float* quality_score);

    DLLEXPORT void destroy_clarity_quality_checker(void* p_clarity_quality_checker);

    // pose quality
    DLLEXPORT void* create_pose_quality_checker();

    DLLEXPORT void check_pose_quality(
        void* p_pose_quality_checker,
        int img_h,
        int img_w,
        int img_c,
        unsigned char* img_data,
        int face_rect[4],
        double face_landmarks[10],
        int* quality_level,
        float* quality_score);

    DLLEXPORT void destroy_pose_quality_checker(void* p_pose_quality_checker);

    // pose estimation
    DLLEXPORT void* create_face_pose_estimator(const char* p_model_file_path);

    DLLEXPORT void estimate_face_pose(
        void* p_face_pose_estimator,
        int img_h,
        int img_w,
        int img_c,
        unsigned char* img_data,
        int face_rect[4],
        float* yaw,
        float* pitch,
        float* roll);

    DLLEXPORT void destroy_face_pose_estimator(void* p_face_pose_estimator);

#ifdef __cplusplus
}
#endif
