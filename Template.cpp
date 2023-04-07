#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <map>
#include <opencv2/opencv.hpp>

using namespace std;

class MemoryLane {
public:
    MemoryLane() {
        // Initialize the memory map.
        memory_map = vector<vector<cv::Mat> >(1000, vector<cv::Mat>(3));
    }

    void add_memory(const cv::Mat& image, const double& latitude, const double& longitude) {
        // Add the image to the memory map.
        memory_map[latitude][longitude] = image;
    }

    void show_memory_map() {
        // Show the memory map.
        for (int i = 0; i < memory_map.size(); i++) {
            for (int j = 0; j < memory_map[i].size(); j++) {
                cv::imshow("Memory", memory_map[i][j]);
                cv::waitKey(0);
            }
        }
    }

private:
    vector<vector<cv::Mat> > memory_map;
};

int main() {
    // Create a memory lane object.
    MemoryLane memory_lane;

    // Load the GPS data.
    vector<double> latitudes;
    vector<double> longitudes;
    {
        ifstream gps_file("gps_data.csv");
        if (gps_file.is_open()) {
            string line;
            while (getline(gps_file, line)) {
                stringstream ss(line);
                double latitude, longitude;
                ss >> latitude >> longitude;
                latitudes.push_back(latitude);
                longitudes.push_back(longitude);
            }
            gps_file.close();
        }
    }

    // Load the image data.
    vector<cv::Mat> images;
    {
        ifstream image_file("image_data.csv");
        if (image_file.is_open()) {
            string line;
            while (getline(image_file, line)) {
                stringstream ss(line);
                int image_id;
                ss >> image_id;
                images.push_back(cv::imread("image_" + to_string(image_id) + ".jpg"));
            }
            image_file.close();
        }
    }

    // Iterate over the GPS data and image data.
    for (int i = 0; i < latitudes.size(); i++) {
        // Add the image to the memory map.
        memory_lane.add_memory(images[i], latitudes[i], longitudes[i]);
    }

    // Show the memory map.
    memory_lane.show_memory_map();

    return 0;
}