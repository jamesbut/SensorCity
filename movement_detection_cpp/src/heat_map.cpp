#include <heat_map.h>

HeatMap::HeatMap(const unsigned WIDTH, const unsigned HEIGHT,
                 const int GROWTH_RATE, const int DECAY_RATE) :
    _WIDTH(WIDTH),
    _HEIGHT(HEIGHT),
    _GROWTH_RATE(GROWTH_RATE),
    _DECAY_RATE(DECAY_RATE),
    _heat_map_img(cv::Mat::zeros(HEIGHT, WIDTH, CV_8UC1)),
    _heat_map(HEIGHT * WIDTH) {}

void HeatMap::increment_heat_map(const cv::Mat& img) {

    for(unsigned i = 0; i < img.rows; i++)
        for(unsigned j = 0; j < img.cols; j++) {

            const unsigned index = i * _WIDTH + j;

            //Increment heat map by _GROWTH_RATE if pixel in img is white
            if(img.at<uchar>(i, j) == 255) {
                if(_heat_map.at(index) + _GROWTH_RATE > 255)
                    _heat_map.at(index) = 255;
                else
                    _heat_map.at(index) += _GROWTH_RATE;
            }

            //Decay pixels over time
            if(_heat_map.at(index) - _DECAY_RATE < 0)
                _heat_map.at(index) = 0;
            else
                _heat_map.at(index) -= _DECAY_RATE;


            //Set image value
            _heat_map_img.at<uchar>(i, j) = static_cast<uchar>(_heat_map.at(index));

        }

}
