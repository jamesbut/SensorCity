#include <iostream>
#include "opencv2/opencv.hpp"
#include <heat_map.h>

int main(int argc, const char* argv[]) {

	//Open camera
	cv::VideoCapture cap(0);	
	if(!cap.isOpened()) {
		std::cout << "Could not open camera" << std::endl;
		return -1;
	}

	//Define window sizes
	//const unsigned WIDTH = 320;
	//const unsigned HEIGHT = 240;
	//cap.set(cv::CAP_PROP_FRAME_WIDTH, WIDTH);
	//cap.set(cv::CAP_PROP_FRAME_HEIGHT, HEIGHT);

/*
	//Set up window positions
	cv::namedWindow("Raw");	
	cv::moveWindow("Raw", 0, 0);
	cv::namedWindow("Gray");	
	cv::moveWindow("Gray", 400, 0);
	cv::namedWindow("Gauss");	
	cv::moveWindow("Gauss", 800, 0);
	cv::namedWindow("Delta");	
	cv::moveWindow("Delta", 0, 350);
	cv::namedWindow("Threshold");	
	cv::moveWindow("Threshold", 400, 350);
*/

	//Previous frame for frame differences
	cv::Mat prev_frame;
	cv::Mat frame0, frame1, frame2, frame3, frame4, frame5;

	while(true) {

		//Get raw image
		cap >> frame0;		

		//Turn image to gray
		cv::cvtColor(frame0, frame1, cv::COLOR_BGR2GRAY);

		//Apply gaussian blur
		cv::GaussianBlur(frame1, frame2, cv::Size(21, 21), 0);

		//Initialise previous frame
		if(prev_frame.empty()) {
			frame2.copyTo(prev_frame);
			continue;
		}

		//Delta frame
		cv::absdiff(prev_frame, frame2, frame3);	

		//Threshold frame
		cv::threshold(frame3, frame4, 15, 255, cv::THRESH_BINARY);	
	
		//Update previous frame
		frame2.copyTo(prev_frame);
		
		cv::imshow("Raw", frame0);
		cv::imshow("Gray", frame1);
		cv::imshow("Gauss", frame2);
		cv::imshow("Delta", frame3);
		cv::imshow("Threshold", frame4);

		if(cv::waitKey(30) >= 0) break;
	
	}	

	return 0;

}
