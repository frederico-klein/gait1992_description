#!/usr/bin/env python3
#http://wiki.ros.org/tf/Tutorials/Writing%20a%20tf%20listener%20%28Python%29

import rospy
#import math
from numpy.linalg import norm
from dynamic_reconfigure.server import Server
from gait1992_description.cfg import FixHeadingConfig
import tf
from geometry_msgs.msg import Quaternion
import sys

br = tf.TransformBroadcaster()

def send_zero():
    callback({"yaw":0},None)

def callback(config, level):
    rospy.loginfo("""Reconfigure Request:
            y:{yaw},\ 
            """.format(**config))
    # normalize quaternion
        ## okay, roll pitch and yaw and Euler angles are different things, this is likely not going to work from the get-go
    q_rot = tf.transformations.quaternion_from_euler(0, 0, config["yaw"])
    # now we broadcast this heading
    br.sendTransform((0,0,0), q_rot, rospy.Time.now(), "pelvis_heading_frame", "map" )
    print(config)
    return config

if __name__ == '__main__':
    try:
        rospy.init_node('heading_correction_server')
        rospy.loginfo("Waiting for dynamic_reconfigure calls at: %s"%rospy.get_name())
        send_zero()
        srv = Server(FixHeadingConfig, callback)
        rospy.spin()
    except rospy.ROSException as e:
        rospy,logerr("something wrong happened %s"%e)
        

