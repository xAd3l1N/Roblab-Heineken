cmake_minimum_required(VERSION 3.0.2)
project(actions_quiz_pkg)

find_package(catkin REQUIRED COMPONENTS
  rospy
  actionlib
  actionlib_msgs
  std_msgs
)

add_action_files(
  DIRECTORY src
  FILES
  DroneAction.action
)

generate_messages(
  DEPENDENCIES
  actionlib_msgs
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS rospy actionlib actionlib_msgs std_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  src/drone_action_server.py
  src/drone_action_client.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
