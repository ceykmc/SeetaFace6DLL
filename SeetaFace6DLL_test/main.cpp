#include <iostream>
#include <opencv2/opencv.hpp>
#include "quality.h"

int main()
{
    const char* query_img_path = "C:\\Users\\xzy_lijun\\Desktop\\faces\\3\\126-1060-309-152-111_1_.png";
    cv::Mat image = cv::imread(query_img_path);
    int face_rect[4] = { 0, 0, image.cols, image.rows };
    double face_landmarks[10] = { 
        33.8604, 50.8867, 70.4262, 56.923, 44.2245, 74.5922, 39.8662, 88.8391, 68.6998, 92.397 
    };
    int level = 0;
    float score = 0;

    void* p_clarity_quality_checker = create_clarity_quality_checker();
    check_clarity_quality(
        p_clarity_quality_checker, int(image.rows), int(image.cols), int(image.channels()),
        image.data, face_rect, face_landmarks, &level, &score);
    destroy_clarity_quality_checker(p_clarity_quality_checker);
    std::cout << "clarity quality, level is: " << level << ", score is: " << score << std::endl;

    void* p_pose_quality_checker = create_pose_quality_checker();
    check_pose_quality(
        p_pose_quality_checker, int(image.rows), int(image.cols), int(image.channels()),
        image.data, face_rect, face_landmarks, &level, &score);
    destroy_pose_quality_checker(p_pose_quality_checker);
    std::cout << "pose quality, level is: " << level << ", score is: " << score << std::endl;

    system("pause");
    return 0;
}
