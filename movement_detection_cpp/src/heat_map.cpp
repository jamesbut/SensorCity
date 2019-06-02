#include <heat_map.h>

HeatMap::HeatMap(const unsigned WIDTH, const unsigned HEIGHT) :
	_WIDTH(WIDTH),
	_HEIGHT(HEIGHT),
	_heat_map(std::vector<int>(WIDTH * HEIGHT, 0)) {}

void HeatMap::increment_heat_map(const cv::Mat& img) {}
