#! /usr/bin/env python
import rospy
import time
import actionlib
from geometry_msgs.msg import Twist, Pose
from ros_summary_project.msg import ActionServerAction, ActionServerGoal, ActionServerResult, ActionServerFeedback
from nav_msgs.msg import Odometry

current_pose = Pose()

def callback(msg):
    global current_pose
    current_pose = msg.pose.pose

def is_get_goal(a,b,c):
    #if(abs(a.position.x-b.position.x) < abs(c.linear.x)):
     #   return False
    #elif(abs(a.position.y-b.position.y) < abs(c.linear.y)):
     #   return False
    #elif(abs(a.position.z-b.position.z) < abs(c.linear.z)):
     #   retturn False
    #elif(abs(a.orientation.x-b.orientation.x) < abs(c.angular.x)):
     #   return False
    #elif(abs(a.orientation.y-b.orientation.y) < abs(c.angular.y)):
     #   return False
    print str(a.orientation.z)
    print str(b.orientation.z)
    print str(c.angular.z)

    if(abs(a.orientation.z - b.orientation.z - c.angular.z) > 0.3):
        return False
    else:
        return True

def get_twist(current_pose, start_pose):
    c = Twist()
    #c.linear.x = current_pose.position.x-start_pose.position.x
    #c.linear.y = current_pose.position.y-start_pose.position.y
    #c.linear.z = current_pose.position.z-start_pose.position.z
    #c.angular.x = current_pose.orientation.x-start_pose.orientation.x
    #c.angular.y = current_pose.orientation.y-start_pose.orientation.y
    c.angular.z = current_pose.orientation.z-start_pose.orientation.z
    return c

def do_action(goal):
    global current_pose

    start_time = time.time()
    # move subscription to module level and remove duplicate
    start_pose = current_pose
    update_count = 0
    speed = Twist()
    speed.angular.z = 0.3
    pub.publish(speed)
    while not is_get_goal(current_pose, start_pose, goal.angle_to_change):
        #odom_sub = rospy.Subscriber('odom', Odometry, callback)
        if server.is_preempt_requested():
            result = ActionServerResult()
            result.angle_changed = get_twist(current_pose, start_pose)
            result.updates_sent = update_count
            server.set_preempted(result, "ActionServer preempted")

        feedback = ActionServerFeedback()
        feedback.angle_changed = get_twist(current_pose, start_pose)

        server.publish_feedback(feedback)
        update_count += 1

        #how to tell robot to spin

        #time.sleep(1.0)
        
    speed.angular.z = 0.0
    print 'stop!!!!' + str(speed.angular.z)
    pub.publish(speed)

    result = result = ActionServerResult()
    result.angle_changed = get_twist(current_pose, start_pose)
    result.updates_sent = update_count
    server.set_succeeded(result, "ActionServer completed successfully")


rospy.init_node('ActionServer')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
server = actionlib.SimpleActionServer('actionServer', ActionServerAction, do_action, False)
odom_sub = rospy.Subscriber('odom', Odometry, callback)
server.start()
rospy.spin()