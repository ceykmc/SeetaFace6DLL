#include "face_quality.h"

void* create_clarity_quality_checker()
{
    return (void*)(new seeta::QualityOfClarity);
}

void destroy_clarity_quality_checker(void* p_clarity_quality_checker)
{
    if (p_clarity_quality_checker) {
        delete (seeta::QualityOfClarity*)p_clarity_quality_checker;
    }
}

void check_clarity_quality(
    void* p_clarity_quality_checker,
    const SeetaImageData& image,
    const SeetaRect& rect,
    const SeetaPointF* landmarks,
    int* quality_level,
    float* quality_score)
{
    seeta::QualityResult result = \
        ((seeta::QualityOfClarity*)p_clarity_quality_checker)->check(image, rect, landmarks, 5);
    *quality_level = int(result.level);
    *quality_score = float(result.score);
}

void* create_pose_quality_checker()
{
    return (void*)(new seeta::QualityOfPose);
}

void destroy_pose_quality_checker(void* p_pose_quality_checker)
{
    if (p_pose_quality_checker) {
        delete (seeta::QualityOfPose*)p_pose_quality_checker;
    }
}

void check_pose_quality(
    void* p_pose_quality_checker,
    const SeetaImageData& image,
    const SeetaRect& rect,
    const SeetaPointF* landmarks,
    int* quality_level,
    float* quality_score)
{
    seeta::QualityResult result = \
        ((seeta::QualityOfPose*)p_pose_quality_checker)->check(image, rect, landmarks, 5);
    *quality_level = int(result.level);
    *quality_score = float(result.score);
}
