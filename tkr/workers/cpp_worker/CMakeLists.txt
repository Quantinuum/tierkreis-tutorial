cmake_minimum_required(VERSION 3.10)
project(tkr_cpp_worker CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Dependencies package
find_package(nlohmann_json REQUIRED)
# Add an include directory for the json library
include_directories(.)

# Add the executable
add_executable(CPPWorker main.cpp)
target_link_libraries(CPPWorker PRIVATE nlohmann_json::nlohmann_json)
set_target_properties(CPPWorker PROPERTIES OUTPUT_NAME "tkr-cpp-worker")

# A message to show where the executable will be
message(STATUS "Executable will be created at ${CMAKE_BINARY_DIR}/tkr-cpp-worker")
install(TARGETS CPPWorker DESTINATION ${CMAKE_SOURCE_DIR})
