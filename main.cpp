#include<opencv2/opencv.hpp>
#include<opencv2/highgui.hpp>
#include<iostream>
using namespace std;
using namespace cv;
int main() {
	VideoCapture cap(0);
	if (!cap.isOpened()) {
		cout << "schimba camera";
		return -1;
	}
	while (true) {
		Mat frame;
		cap.read(frame);
			cap.read(frame);
		imshow("camera", frame);
		if (waitKey(30) == 27){
			return 0; 
		
		}
	}
}