#!/usr/bin/env python

"""
    ros_tcp_comm Sender Node

    Authors: Nicholas McCullough and Joseph Neidigh

    Faculty Advisor: Dr. Nathan Sprague

    Version 1.0

    This node sends messages across a wireless network via a TCP connection.
    It is intended to send these messages to the corresponding 'Receiver' node
    in this package. Instructions for how to customize this node to subscribe to
    and send a particular topic are as follows:

        Step 1: Import the appropriate message type. This should match the message type
                that is being published to the topic to be sent. In this example the 
                topic to be sent is a simple topic that publishes a std_msgs/String 
                message. This topic can be generated by running the following command in
                a terminal after the ROS core is already running:
                    'rostopic pub /topic_to_send std_msgs/String "Hello World" -r 1 &'

        Step 2: Set up a subscriber to receive the messages from the original topic. The
                second argument should match the message type that was imported in Step 1.
                The messages will be sent to the reveiver in the callback method passed as
                the third argument.

        Step 3: Pass the desired field of the message received by the callback into 'pickle.dumps()'.
                Entire messages cannot be sent but fields consisting of primitive data types can be.
"""

import socket
import pickle
import sys
import struct
import zlib
import rospy
# Step 1 ######################
from std_msgs.msg import String
###############################

class Sender():
    def __init__(self):
        rospy.init_node('sender')
        # Step 2 ##############################################################
        rospy.Subscriber('/topic_to_send', String, self.callback, queue_size=1)
        #######################################################################

        RECEIVER_IP = "127.0.0.1"
        PORT = 13000

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((RECEIVER_IP, PORT))
        except Exception as e:
            sock.close()
            rospy.loginfo("SENDER ERROR")
            rospy.loginfo(e)
            sys.exit()
        
        rospy.spin()

    def callback(self, topic_message):
        # Step 3 #################################
        message = pickle.dumps(topic_message.data)
        ##########################################
        compressed_message = zlib.compress(message)
        self.send_msg(compressed_message)

    def send_msg(self, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        try:
            self.sock.sendall(msg)
        except Exception as e:
            self.sock.close()
            rospy.loginfo("SENDER ERROR")
            rospy.loginfo(e)
            sys.exit()

if __name__ == "__main__":
    Sender()