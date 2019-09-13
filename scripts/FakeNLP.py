#!/usr/bin/env python

import rospy
import re
from ros_summary_project.srv import FakeNLP, FakeNLPResponse
from ros_summary_project.msg import command

def parseCommand(request):
    print("Responding to a request for: "+request.inputs)
    commandLine = request.inputs
    digits = re.findall("[-+]?\d*\.\d+|\d+", commandLine)
    if(len(digits) == 1):
       return FakeNLPResponse(float(digits[0]))
    else:
       return FakeNLPResponse()

rospy.init_node('FakeNLP')

service = rospy.Service('FakeNLP', FakeNLP, parseCommand)

rospy.spin()