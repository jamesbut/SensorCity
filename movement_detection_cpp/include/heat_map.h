#ifndef _HEAT_MAP_H_
#define _HEAT_MAP_H_

#include <vector>
#include <opencv2/opencv.hpp>

class HeatMap {

public:
	
	HeatMap(const unsigned WIDTH, const unsigned HEIGHT);

	//Take a binary image and increment the map with the image
	void increment_heat_map(const cv::Mat& img);

private:

	const unsigned _WIDTH;
	const unsigned _HEIGHT;

	//Using 1D vector for speed
	std::vector<int> _heat_map;

};

#endif
