#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

def callback(msg):
    moveHeineken = Twist()
    
    fata = msg.ranges[0]
    stanga = msg.ranges[90]
    dreapta = msg.ranges[270]

    if fata > 1.0:
        moveHeineken.linear.x = 0.2
        moveHeineken.angular.z = 0.0
    
    if fata <= 1.0:
        moveHeineken.linear.x = 0.0
        moveHeineken.angular.z = 1

    if dreapta < 1.0:
        moveHeineken.linear.x = 0.0
        moveHeineken.angular.z = 1

    if stanga < 1.0:
        moveHeineken.linear.x = 0.0
        moveHeineken.angular.z = -1

    pub.publish(moveHeineken)

rospy.init_node('topics_quiz_node')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
sub = rospy.Subscriber('/scan', LaserScan, callback)
rospy.spin()
