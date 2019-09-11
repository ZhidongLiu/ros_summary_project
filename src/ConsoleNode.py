#!/usr/bin/env python

import rospy
from ros_summary_project.msg import command

rospy.init_node('ConsoleNode')

pub = rospy.Publisher('/demo/command', command, queue_size = 10)

consoleInput = command()

consoleInput.command = raw_input("Please enter your command:")

rate = rospy.Rate(2)
while not rospy.is_shutdown():
    pub.publish(consoleInput)
    rate.sleep()


