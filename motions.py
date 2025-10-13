# Imports
import rclpy

from rclpy.node import Node

from utilities import Logger, euler_from_quaternion
from rclpy.qos import QoSProfile

# Import ROS2 message types for robot control and sensor data
from geometry_msgs.msg import Twist  # For sending velocity commands
from sensor_msgs.msg import Imu  # For IMU (accelerometer/gyroscope) data
from sensor_msgs.msg import LaserScan  # For laser range finder data
from nav_msgs.msg import Odometry  # For position/orientation estimates

from rclpy.time import Time

# Motion type constants for better code readability
CIRCLE=0; SPIRAL=1; ACC_LINE=2
motion_types=['circle', 'spiral', 'line']
LINEAR_VELOCITY = 0.1  # m/s - forward speed
ANGULAR_VELOCITY = 0.5  # rad/s - rotation speed

class motion_executioner(Node):
    # ROS2 node that executes different motion patterns for a mobile robot
    # while logging sensor data from IMU, odometry, and laser scanner.
    
    def __init__(self, motion_type=0):
        super().__init__("motion_types")
        
        self.type=motion_type
        
        # Variables for spiral motion
        self.radius_=0.0  # Initial radius (will increase over time)
        self.linear_speed =0.0  # Current speed for accelerated line
        self.accel_lin = 0.05  # Acceleration rate for line motion
        
        # Initialization flags to ensure all sensors are ready before moving
        self.successful_init=False
        self.imu_initialized=False
        self.odom_initialized=False
        self.laser_initialized=False
        
        # Publisher for velocity commands (controls robot movement)
        self.vel_publisher=self.create_publisher(Twist, '/cmd_vel', 10)
                
        # Create CSV loggers for each sensor type
        self.imu_logger=Logger('imu_content_'+str(motion_types[motion_type])+'.csv', 
                               headers=["acc_x", "acc_y", "angular_z", "stamp"])
        self.odom_logger=Logger('odom_content_'+str(motion_types[motion_type])+'.csv', 
                                headers=["x","y","th", "stamp"])
        self.laser_logger=Logger('laser_content_'+str(motion_types[motion_type])+'.csv', 
                                 headers=["ranges", "angle_increment", "stamp"])
        
        # QoS (Quality of Service) profile for reliable sensor data reception
        # reliability=2: RELIABLE (ensures messages arrive)
        # durability=2: TRANSIENT_LOCAL (stores messages for late joiners)
        # history=1: KEEP_LAST (keep only recent messages)
        # depth=10: keep last 10 messages in queue
        qos=QoSProfile(reliability=2, durability=2, history=1, depth=10)

        # Subscribe to sensor topics to receive data
        # IMU subscription - provides acceleration and angular velocity
        self.create_subscription(Imu, '/imu', self.imu_callback, qos_profile=qos)

        # Odometry subscription - provides position and orientation estimates
        self.create_subscription(Odometry, '/odom', self.odom_callback, qos_profile=qos)

        # LaserScan subscription - provides distance measurements in 360 degrees
        self.create_subscription(LaserScan, '/scan', self.laser_callback, qos_profile=qos)
        
        # Timer callback runs at 10Hz (every 0.1 seconds) to control robot motion
        self.create_timer(0.1, self.timer_callback)

    def imu_callback(self, imu_msg: Imu):
        # Process incoming IMU data and log it.
        # IMU provides linear acceleration and angular velocity measurements.
        
        self.imu_initialized=True

        # Extract timestamp in nanoseconds (ROS2 standard time format)
        timestamp = Time.from_msg(imu_msg.header.stamp).nanoseconds

        # Extract relevant IMU measurements
        # Linear acceleration in x and y directions (m/s^2)
        imu_acc_x = imu_msg.linear_acceleration.x
        imu_acc_y = imu_msg.linear_acceleration.y
        # Angular velocity around z-axis (rotation speed, rad/s)
        imu_angular_z = imu_msg.angular_velocity.z

        # Combine data into list and log
        imu_data_list = [imu_acc_x, imu_acc_y, imu_angular_z, timestamp]
        self.imu_logger.log_values(imu_data_list)

    def odom_callback(self, odom_msg: Odometry):
        # Process incoming odometry data and log it.
        # Odometry provides estimated position and orientation based on wheel encoders.

        self.odom_initialized=True

        # Extract timestamp
        timestamp = Time.from_msg(odom_msg.header.stamp).nanoseconds

        # Extract position (x, y coordinates in meters)
        odom_x_pos = odom_msg.pose.pose.position.x
        odom_y_pos = odom_msg.pose.pose.position.y
        
        # Extract orientation (quaternion) and convert to yaw angle
        # Quaternion provides 3D orientation; we only need yaw (rotation around z-axis)
        odom_q = odom_msg.pose.pose.orientation
        odom_orientation = euler_from_quaternion([odom_q.x, odom_q.y, odom_q.z, odom_q.w])

        # Combine data into list and log
        odom_data_list = [odom_x_pos, odom_y_pos, odom_orientation, timestamp]
        self.odom_logger.log_values(odom_data_list)

    def laser_callback(self, laser_msg: LaserScan):
        # Process incoming laser scan data and log it.
        # Laser scanner provides distance measurements at different angles around the robot.
        
        self.laser_initialized=True

        # Extract timestamp
        timestamp = Time.from_msg(laser_msg.header.stamp).nanoseconds

        # Extract laser scan data
        # ranges: array of distance measurements (one per angle)
        # angle_increment: angular separation between consecutive measurements
        ranges = laser_msg.ranges
        angle_increment = laser_msg.angle_increment

        # Combine data into list and log
        laser_data_list = [ranges, angle_increment, timestamp]
        self.laser_logger.log_values(laser_data_list)
                
    def timer_callback(self):
        # Main control loop - executes at 10Hz to control robot motion.
        # Only starts moving once all sensors have sent at least one message.

        # Wait until all sensors have initialized before moving the robot
        if self.odom_initialized and self.laser_initialized and self.imu_initialized:
            self.successful_init=True
            
        if not self.successful_init:
            return
        
        # Create velocity command message
        cmd_vel_msg=Twist()
        
        # Generate appropriate motion based on selected type
        if self.type==CIRCLE:
            cmd_vel_msg=self.make_circular_twist()
            print(cmd_vel_msg)
        elif self.type==SPIRAL:
            cmd_vel_msg=self.make_spiral_twist()
        elif self.type==ACC_LINE:
            cmd_vel_msg=self.make_acc_line_twist()
        else:
            print("type not set successfully, 0: CIRCLE 1: SPIRAL and 2: ACCELERATED LINE")
            raise SystemExit 

        # Publish the velocity command to move the robot
        self.vel_publisher.publish(cmd_vel_msg)
        
    def make_circular_twist(self):
        # Generate velocity command for circular motion.
        # Constant forward velocity + constant angular velocity = circular path.
        # The radius of the circle is determined by: r = linear_velocity / angular_velocity
        
        msg=Twist()
        # Constant forward velocity
        msg.linear.x = LINEAR_VELOCITY
        # Constant rotational velocity (positive = counterclockwise)
        msg.angular.z = ANGULAR_VELOCITY
        return msg

    def make_spiral_twist(self):
        # Generate velocity command for spiral motion.
        # Constant forward velocity with decreasing angular velocity = expanding spiral.
        # As radius increases, angular velocity decreases to maintain smooth motion.

        msg=Twist()
        # Constant forward velocity
        msg.linear.x = LINEAR_VELOCITY
        # Gradually increase the radius of the spiral
        self.radius_ += 0.1
        # Calculate angular velocity: ω = v/r (decreases as radius increases)
        msg.angular.z = msg.linear.x / self.radius_
        return msg
    
    def make_acc_line_twist(self):
        # Generate velocity command for accelerated linear motion.
        # Forward velocity increases over time; no rotation.

        # Increase speed by acceleration amount each time step
        self.linear_speed += self.accel_lin
        msg=Twist()
        # Set forward velocity (accumulates over time)
        msg.linear.x += self.linear_speed
        # No rotation (straight line)
        msg.angular.z = 0.0
        return msg

import argparse

if __name__=="__main__":
    # Main entry point - parse command line arguments and start the ROS2 node.

    argParser=argparse.ArgumentParser(description="input the motion type")
    argParser.add_argument("--motion", type=str, default="circle")

    # Initialize ROS2
    rclpy.init()

    args = argParser.parse_args()

    # Create the motion executioner node with the requested motion type
    if args.motion.lower() == "circle":
        ME=motion_executioner(motion_type=CIRCLE)
    elif args.motion.lower() == "line":
        ME=motion_executioner(motion_type=ACC_LINE)
    elif args.motion.lower() =="spiral":
        ME=motion_executioner(motion_type=SPIRAL)
    else:
        print(f"we don't have {args.motion.lower()} motion type")

    # Run the node until interrupted
    try:
        rclpy.spin(ME)
    except KeyboardInterrupt:
        print("Exiting")