#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn
import math

x1, y1, yaw1 = 0, 0, 0 #Turtle 1
x2, y2, yaw2 = 0, 0, 0 #Turtle 2

def poseCallbackTurtle1(pose_message):
    global x1, y1, yaw1
    x1 = pose_message.x
    y1 = pose_message.y
    yaw1 = pose_message.theta

def poseCallbackTurtle2(pose_message):
    global x2, y2, yaw2
    x2 = pose_message.x
    y2 = pose_message.y
    yaw2 = pose_message.theta

def setUpPose():
    position_topic = '/turtlesim1/turtle1/pose'
    pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallbackTurtle1)
    position_topic2 = '/turtlesim1/turtle2/pose'
    pose_subscriber = rospy.Subscriber(position_topic2, Pose, poseCallbackTurtle2)

def move():
    velocity_message = Twist()
    rate = rospy.Rate(10) # 10hz
    cmd_vel_topic = '/turtlesim1/turtle2/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
    while not rospy.is_shutdown():
        rospy.loginfo(y2-y1)
        
        dist = abs(math.sqrt((x1-x2)**2 + (y1-y2)**2))
        if dist < 0.05:
            velocity_message.linear.x = 0 #Stop
            velocity_message.angular.z = 0
        else:
            velocity_message.linear.x = 1 #Move forwards
            velocity_message.angular.z = math.atan2(y1-y2, x1-x2) - yaw2 #Face towards 1

        velocity_publisher.publish(velocity_message)
        rate.sleep()
        
def spawnTurtle():
    spawnFunc = rospy.ServiceProxy('/turtlesim1/spawn', Spawn)
    spawnFunc(1, 1, 0, "turtle2")


if __name__ == '__main__':
    try:
        rospy.init_node('turtlesim_motion_pose', anonymous=True)

        spawnTurtle()
        setUpPose()
        move()


    except rospy.ROSInterruptException:
        pass
