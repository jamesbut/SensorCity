#include <heat_map.h>

HeatMap::HeatMap(const unsigned WIDTH, const unsigned HEIGHT) :
	_WIDTH(WIDTH),
	_HEIGHT(HEIGHT),
	_heat_map(cv::Mat::zeros(HEIGHT, WIDTH, CV_8UC1)) {}

void HeatMap::increment_heat_map(const cv::Mat& img) {

	for(unsigned i = 0; i < img.rows; i++) 	
		for(unsigned j = 0; j < img.cols; j++)
			if(img.at<uchar>(i, j) == 255)
				_heat_map.at<uchar>(i, j) += 1; 

}
