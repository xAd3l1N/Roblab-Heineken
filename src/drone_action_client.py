#!/usr/bin/env python3

import rospy
import actionlib
import sys
from actions_quiz_pkg.msg import DroneActionAction, DroneActionGoal

def feedback_cb(feedback):
    rospy.loginfo("Feedback: " + feedback.status)

rospy.init_node('drone_action_client_node')

client = actionlib.SimpleActionClient('drone_action_server', DroneActionAction)
client.wait_for_server()

goal = DroneActionGoal()

if len(sys.argv) > 1:
    goal.command = sys.argv[1]
else:
    goal.command = "TAKEOFF"

rospy.loginfo("Sending goal: " + goal.command)
client.send_goal(goal, feedback_cb=feedback_cb)

client.wait_for_result()

rospy.loginfo("Result state: %d" % client.get_state())
