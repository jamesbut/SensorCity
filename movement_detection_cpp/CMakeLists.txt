cmake_minimum_required(VERSION 3.11.4)

set(CMAKE_CXX_STANDARD 17)

find_package(OpenCV REQUIRED)

include_directories(
	include
	${OpenCV_INCLUDE_DIRS}
)
	

file(GLOB_RECURSE SOURCES "src/*.cpp")

add_executable(movement_detection ${SOURCES})

target_link_libraries(movement_detection
	${OpenCV_LIBS}	
)
