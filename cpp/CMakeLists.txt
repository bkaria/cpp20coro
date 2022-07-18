cmake_minimum_required (VERSION 3.2)
project(tcpproxy VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


set(EXTERNAL_ROOT "/home/ubuntu/build/exchange/release/externalprojects/")
set(Boost_ROOT ${EXTERNAL_ROOT}/boost)
set(Boost_INCLUDE_DIRS ${Boost_ROOT}/include)
set(Boost_LIBRARY_DIRS ${Boost_ROOT}/lib/)

add_definitions(-DBOOST_STACKTRACE_USE_NOOP)
include_directories( ${Boost_INCLUDE_DIRS} )

find_package(Threads REQUIRED)
find_library( LIB_RT rt )

add_executable(tcpproxy-c20
    tcpproxy-c20.cpp
)
target_link_libraries(tcpproxy-c20 ${CMAKE_THREAD_LIBS_INIT})

add_executable(tcpproxy-cb
    tcpproxy-cb.cpp
)
target_link_libraries(tcpproxy-cb ${CMAKE_THREAD_LIBS_INIT})

message( STATUS "Boost_INCLUDE_DIRS: " ${Boost_INCLUDE_DIRS} )
message( STATUS "Boost_LIBRARY_DIRS: " ${Boost_LIBRARY_DIRS} )

