import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String
from sensor_msgs.msg import Image

import cv2
import numpy as np
from cv_bridge import CvBridge


class RealSenseSubscriber(Node):
  def __init__(self):
    super().__init__("realsense_subscriber")
    qos_profiile = QoSProfile(depth=10)
    self.rgb_subscriber = self.create_subscription(
      Image,
      "camera/color/image_rect_raw",
      self.rgb_frame_callback,
      qos_profiile)
    self.br_rgb = CvBridge()
    
  def rgb_frame_callback(self, data):
    self.get_logger().warning("Receiving RGB frame")
    current_frame = self.br_rgb.imgmsg_to_cv2(data, 'bgr8')
    cv2.imshow("rgb", current_frame)
    cv2.waitKey(1)

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