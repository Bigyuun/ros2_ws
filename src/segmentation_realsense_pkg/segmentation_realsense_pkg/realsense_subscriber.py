import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from sensor_msgs.msg import Imu

from rclpy.action import ActionServer
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy

import cv2
import numpy as np
from cv_bridge import CvBridge

g_depth = 10
g_frame_shape = (480, 640, 3)
class RealSenseSubscriber(Node):
  """_summary_
  author - DY
  Inter(R) RealSense Subscriber Node
  It premise that you use the 'Depth' Camera.
  """

  def __init__(self):
    """_summary_
    ROS2 QoS setup and making subscriber for each topics.
    """
    super().__init__("realsense_subscriber")
    qos_profiile = QoSProfile(depth=g_depth)
    self.rgb_frame = np.zeros(g_frame_shape)
    self.callback_group = ReentrantCallbackGroup()

    ## Camera calibration and metadata
    self.color_camera_info_subscriber = self.create_subscription(
      CameraInfo,
      "color/camera_info",
      self.color_camera_info_callback,
      qos_profiile)

    ## color rectified image. RGB format
    self.color_image_rect_raw_subscriber = self.create_subscription(
      Image,
      "color/image_rect_raw",
      self.color_image_rect_raw_callback,
      qos_profiile)

    ## Camera calibration and metadata
    self.depth_camera_info_subscriber = self.create_subscription(
      CameraInfo,
      "depth/camera_info",
      self.depth_camera_info_callback,
      qos_profiile)

    ## Raw image from device. Contains uint16depth in mm.
    self.depth_image_rect_raw_subscriber = self.create_subscription(
      Image,
      "depth/image_rect_raw",
      self.depth_image_rect_raw_callback,
      qos_profiile)

    self.imu_subscriber = self.create_subscription(
      Imu,
      "imu",
      self.imu_callback,
      qos_profiile)

    self.br_rgb = CvBridge()


  def color_camera_info_callback(self, data):
    return

  def color_image_rect_raw_callback(self, data):
    self.get_logger().info("Receiving RGB frame")
    current_frame = self.br_rgb.imgmsg_to_cv2(data, 'bgr8')
    # print(current_frame.shape)
    self.rgb_frame = np.resize(current_frame, g_frame_shape)
    # cv2.imshow("rgb", current_frame)
    cv2.imshow("rgb", self.rgb_frame)
    print(self.rgb_frame.shape)

    cv2.waitKey(1)
    return

  def depth_camera_info_callback(self, data):
    return

  def depth_image_rect_raw_callback(self, data):
    return

  def imu_callback(self, data):
    return


def main(args=None):
  rclpy.init(args=args)
  node = RealSenseSubscriber()
  try:
    rclpy.spin(node)
  except KeyboardInterrupt:
    node.get_logger().info('Keyboard Interrupt (SIGINT)')
  finally:
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main":
  main()
