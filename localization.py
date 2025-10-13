import sys

from utilities import Logger, euler_from_quaternion
from rclpy.time import Time
from rclpy.node import Node

from rclpy.qos import QoSProfile
from nav_msgs.msg import Odometry as odom

from rclpy import init, spin

rawSensor = 0
class localization(Node):
    
    def __init__(self, localizationType=rawSensor):

        super().__init__("localizer")
        
        # TODO Part 3: Define the QoS profile variable based on whether you are using the simulation (Turtlebot 3 Burger) or the real robot (Turtlebot 4)
        # Remember to define your QoS profile based on the information available in "ros2 topic info /odom --verbose" as explained in Tutorial 3

        # TurtleBot 4
        # QoS profile for high-frequency sensor data
        # reliability=0: BEST_EFFORT (prioritizes low latency over guaranteed delivery)
        # durability=2: VOLATILE (only sends to current subscribers, no stored messages)
        # history=1: KEEP_LAST (keep only recent messages)
        # depth=10: keep last 10 messages in queue
        odom_qos = QoSProfile(reliability=0, durability=2, history=1, depth=10)
        
        # TurtleBot 3 Burger for simulation
        # QoS profile for simulated sensor data
        # reliability=2: RELIABLE (ensures all messages arrive, acceptable in simulation)
        # durability=2: VOLATILE (only sends to current subscribers, no stored messages)
        # history=1: KEEP_LAST (keep only recent messages)
        # depth=10: keep last 10 messages in queue
        # odom_qos = QoSProfile(reliability=2, durability=2, history=1, depth=10)

        self.loc_logger=Logger("robot_pose.csv", ["x", "y", "theta", "stamp"])
        self.pose=None
        
        if localizationType == rawSensor:
        # TODO Part 3: subscribe to the position sensor topic (Odometry)

            # Odometry subscription - provides position and orientation estimates
            self.create_subscription(odom, '/odom', self.odom_callback, qos_profile=odom_qos)

        else:
            print("This type doesn't exist", sys.stderr)
    
    
    def odom_callback(self, pose_msg):
        
        # TODO Part 3: Read x,y, theta, and record the stamp

        # Extract timestamp
        timestamp = pose_msg.header.stamp

        # Extract position (x, y coordinates in meters)
        odom_x_pos = pose_msg.pose.pose.position.x
        odom_y_pos = pose_msg.pose.pose.position.y
        
        # Extract orientation (quaternion) and convert to yaw angle
        odom_q = pose_msg.pose.pose.orientation
        odom_orientation = euler_from_quaternion([odom_q.x, odom_q.y, odom_q.z, odom_q.w])

        # Combine data into list
        self.pose = [odom_x_pos, odom_y_pos, odom_orientation, timestamp]
        
        # Log the data
        self.loc_logger.log_values([self.pose[0], self.pose[1], self.pose[2], Time.from_msg(self.pose[3]).nanoseconds])
    
    def getPose(self):
        return self.pose

# TODO Part 3
# Here put a guard that makes the node run, ONLY when run as a main thread!
# This is to make sure this node functions right before using it in decision.py

# Create a Python main guard
if __name__ == "__main__":

    # Initialize ros
    init()

    # Instantiate the localization node
    loc = localization()
    
    # Spin the node
    spin(loc)
