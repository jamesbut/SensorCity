#ifndef _HEAT_MAP_H_
#define _HEAT_MAP_H_

#include <vector>
#include <opencv2/opencv.hpp>

class HeatMap {

public:

    HeatMap(const unsigned WIDTH, const unsigned HEIGHT,
            const int GROWTH_RATE, const int DECAY_RATE);

    //Take a binary image and increment the map with the image
    void increment_heat_map(const cv::Mat& img);

    const cv::Mat& get_heat_map() { return _heat_map_img; };

private:

    const unsigned _WIDTH;
    const unsigned _HEIGHT;

    const int _GROWTH_RATE;
    const int _DECAY_RATE;

    //Use 1D vector for speed
    std::vector<short> _heat_map;

    //Heat map image
    cv::Mat _heat_map_img;

};

#endif
