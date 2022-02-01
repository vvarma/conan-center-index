#include <iostream>
#include <libcamera/camera_manager.h>

int main() {
  auto cm_ = new libcamera::CameraManager();
  std::cout << cm_->version()<<std::endl;
}
