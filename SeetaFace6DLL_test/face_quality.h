#pragma once

#ifdef _WINDLL
#define DLLEXPORT _declspec(dllexport)
#else
#define DLLEXPORT _declspec(dllimport)
#endif

#include <seeta/QualityOfClarity.h>
#include <seeta/QualityOfPose.h>

#ifdef __cplusplus
extern "C" {
#endif
    DLLEXPORT void* create_clarity_quality_checker();

    DLLEXPORT void check_clarity_quality(
        void* p_clarity_quality_checker,
        const SeetaImageData& image,
        const SeetaRect& rect,
        const SeetaPointF* landmarks,
        int* quality_level,
        float* quality_score);

    DLLEXPORT void destroy_clarity_quality_checker(void* p_clarity_quality_checker);

    // pose quality
    DLLEXPORT void* create_pose_quality_checker();

    DLLEXPORT void check_pose_quality(
        void* p_clarity_quality_checker,
        const SeetaImageData& image,
        const SeetaRect& rect,
        const SeetaPointF* landmarks,
        int* quality_level,
        float* quality_score);

    DLLEXPORT void destroy_pose_quality_checker(void* p_pose_quality_checker);

#ifdef __cplusplus
}
#endif

