#!/usr/bin/env python

import rospy
from ros_summary_project.msg import command
from ros_summary_project.srv import FakeNLP
import sys
import actionlib
from geometry_msgs.msg import Twist
from ros_summary_project.msg import ActionServerAction, ActionServerGoal, ActionServerResult, ActionServerFeedback

rospy.init_node('MainNode')

angle_change = None
command_line = None
def callback(msg):
    command_line = msg.command
    rospy.wait_for_service('FakeNLP')
    Fake_NLP = rospy.ServiceProxy('FakeNLP', FakeNLP)
    number_result = Fake_NLP(command_line)
    global angle_change
    angle_change = number_result.number
    print 'number', '->', number_result.number

def feedback_cb(feedback):
    rospy.loginfo('[Feedback] Angle changed: ' + str(feedback.angle_changed))


sub = rospy.Subscriber('/demo/command', command, callback)



client = actionlib.SimpleActionClient('actionServer',ActionServerAction)

rospy.loginfo("Waiting for server...")
client.wait_for_server()

goal = ActionServerGoal()
goal.angle_to_change = Twist()
goal.angle_to_change.angular.z = angle_change

client.send_goal(goal, feedback_cb=feedback_cb)

client.wait_for_result()
rospy.loginfo('[Result] State: %d'%(client.get_state()))
rospy.loginfo('[Result] Status: %s'%(client.get_goal_status_text()))
rospy.loginfo('[Result] Angle changed: %s'%(str(client.get_result().angle_changed)))
rospy.loginfo('[Result] Updates sent: %d'%(client.get_result().updates_sent))
