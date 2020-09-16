#include "quality.h"
#include <seeta/QualityOfPose.h>
#include <seeta/QualityOfClarity.h>

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
    int img_h,
    int img_w,
    int img_c,
    unsigned char* img_data,
    int rect[4],
    double points[10],
    int* level,
    float* score)
{
    SeetaImageData seeta_image = { img_w, img_h, img_c, img_data };
    SeetaRect seeta_rect = { rect[0], rect[1], rect[2], rect[3] };
    SeetaPointF seeta_points[5];
    for (int i = 0; i < 5; ++i) {
        seeta_points[i].x = points[i * 2];
        seeta_points[i].y = points[i * 2 + 1];
    }
    seeta::QualityResult result = \
        ((seeta::QualityOfClarity*)p_clarity_quality_checker)->check(\
            seeta_image, seeta_rect, seeta_points, 5);
    *level = int(result.level);
    *score = float(result.score);
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
    int img_h,
    int img_w,
    int img_c,
    unsigned char* img_data,
    int rect[4],
    double points[10],
    int* level,
    float* score)
{
    SeetaImageData seeta_image = { img_w, img_h, img_c, img_data };
    SeetaRect seeta_rect = { rect[0], rect[1], rect[2], rect[3] };
    SeetaPointF seeta_points[5];
    for (int i = 0; i < 5; ++i) {
        seeta_points[i].x = points[i * 2];
        seeta_points[i].y = points[i * 2 + 1];
    }
    seeta::QualityResult result = \
        ((seeta::QualityOfPose*)p_pose_quality_checker)->check(\
            seeta_image, seeta_rect, seeta_points, 5);
    *level = int(result.level);
    *score = float(result.score);
}
