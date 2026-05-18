#!/usr/bin/env python3

import rospy
import actionlib
from std_msgs.msg import Empty
from actions_quiz_pkg.msg import DroneActionAction, DroneActionFeedback, DroneActionResult

class DroneServer:

    def __init__(self):

        self.takeoff_pub = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)
        self.land_pub = rospy.Publisher('/ardrone/land', Empty, queue_size=1)

        self.server = actionlib.SimpleActionServer(
            'drone_action_server',
            DroneActionAction,
            execute_cb=self.execute_cb,
            auto_start=False
        )

        self.server.start()
        rospy.loginfo("Drone Action Server started")

    def execute_cb(self, goal):

        feedback_HK = DroneActionFeedback()
        result_HK = DroneActionResult()
        rate = rospy.Rate(1)

        command = goal.command.upper()

        if command == "TAKEOFF":

            self.takeoff_pub.publish(Empty())
            rospy.loginfo("Drone taking off")

            while not self.server.is_preempt_requested():
                feedback_HK.status = "TAKING OFF"
                self.server.publish_feedback(feedback_HK)
                rate.sleep()

            self.server.set_preempted()

        elif command == "LAND":

            self.land_pub.publish(Empty())
            rospy.loginfo("Drone landing")

            for i in range(4):
                if self.server.is_preempt_requested():
                    self.server.set_preempted()
                    return
                feedback_HK.status = "LANDING"
                self.server.publish_feedback(feedback_HK)
                rate.sleep()

            self.server.set_succeeded(result_HK)

        else:
            rospy.logwarn("Unknown command: " + command)
            self.server.set_aborted(result_HK)


if __name__ == '__main__':

    rospy.init_node('drone_action_server_node')

    server = DroneServer()

    rospy.spin()
