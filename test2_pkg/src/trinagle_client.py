#! /usr/bin/env python
import rospy
# Import the service message used by the service /trajectory_by_name
from test2_pkg.srv import MoveInTriangle, MoveInTriangleRequest
import sys

# Initialise a ROS node with the name service_client
rospy.init_node('service_client')
# Wait for the service client /move_in_square to be running
rospy.wait_for_service('/move_in_triangle')
# Create the connection to the service
move_in_triangle_service = rospy.ServiceProxy('/move_in_triangle', MoveInTriangle)
# Create an object of type MoveInTriangleRequest
move_in_triangle_object = MoveInTriangleRequest()
move_in_triangle_object.side = 0.5
move_in_triangle_object.repetitions = 2
  
# Send through the connection the name of the request
result = move_in_triangle_service(move_in_triangle_object)
# Print the result given by the service called
print(result)
