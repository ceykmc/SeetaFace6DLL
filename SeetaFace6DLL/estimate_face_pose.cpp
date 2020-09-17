#include "estimate_face_pose.h"

void* create_face_pose_estimator(const char* p_model_file_path)
{
    seeta::ModelSetting::Device device = seeta::ModelSetting::CPU;
    int id = 0;
    seeta::ModelSetting face_pose_model(p_model_file_path, device, id);
    return (void*)new seeta::PoseEstimator(face_pose_model);
}

void destroy_face_pose_estimator(void* p_face_pose_estimator)
{
    if (p_face_pose_estimator) {
        delete (seeta::PoseEstimator*)p_face_pose_estimator;
    }
}

void estimate_face_pose(
    void* p_face_pose_estimator,
    const SeetaImageData& image,
    const SeetaRect& face_rect,
    float* yaw,
    float* pitch,
    float* roll)
{
    ((seeta::PoseEstimator*)p_face_pose_estimator)->Estimate(
        image, face_rect, yaw, pitch, roll);
}
