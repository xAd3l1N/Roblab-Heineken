#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class EvitareObstacol:
    def __init__(self):
        # Inițializăm nodul
        rospy.init_node('nod_evitare_obstacol_heineken')
        
        # Facem publishe pentru /cmd_vel
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        
        # Facem subscriber pentru /scan
        self.sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        
        self.cmd = Twist()
        
    def scan_callback(self, msg):
        # Curățăm datele primite (uneori senzorul întoarce inf sau NaN)
        # Dacă o valoare este sub range_min sau peste range_max, o setăm la 100.0 (fără obstacol)
        ranges = []
        for r in msg.ranges:
            if msg.range_min < r < msg.range_max:
                ranges.append(r)
            else:
                ranges.append(100.0)

        num_ranges = len(ranges)
       
        # Pentru TurtleBot3, senzorul are 360 de valori (0 = Fata, 90 = Stanga, 180 = Spate, 270 = Dreapta)
        # Vom verifica un "con" de +- 30 de grade pentru fiecare directie
        front_ranges = ranges[0:30] + ranges[330:360]
        dist_fata_H = min(front_ranges) if len(front_ranges) > 0 else 100.0
        
        left_ranges = ranges[60:120]
        dist_stanga_H = min(left_ranges) if len(left_ranges) > 0 else 100.0
        
        right_ranges = ranges[240:300]
        dist_dreapta_H = min(right_ranges) if len(right_ranges) > 0 else 100.0
        
        if dist_fata_H < 1.0:
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = 0.5
        elif dist_dreapta_H < 1.0:
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = 0.5
        elif dist_stanga_H < 1.0:
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = -0.5
        else:
            # Niciun obstacol sub 1m in fata/stanga/dreapta -> move forward
            self.cmd.linear.x = 0.2
            self.cmd.angular.z = 0.0
            
        # Publicăm comanda de velocitate
        self.pub.publish(self.cmd)

if __name__ == '__main__':
    try:
        oa = EvitareObstacol()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
