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

# Tensorflow
import os
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
from tqdm import tqdm
import tensorflow as tf
# from sklearn.metrics import f1_score, jaccard_score
# from UNet_train import create_dir, load_dataset

import threading
import time

g_depth = 10
g_frame_shape = (480, 640, 3)

class UNetProcessor(Node):
  """_summary_
  author - DY
  Inter(R) RealSense Subscriber Node
  It premise that you use the 'Depth' Camera.
  """

  def __init__(self):
    """_summary_
    ROS2 QoS setup and making subscriber for each topics.
    """
    # initializing
    super().__init__("unet_process_node")
    qos_profiile = QoSProfile(depth=g_depth)
    print("Unet Process node up to date")
    print("==============================================")
    print("dir_path :",os.getcwd())
    print("==============================================")
    self.image_rect_raw = np.zeros(g_frame_shape)
    self.rgb_frame = np.zeros(g_frame_shape)
    self.depth_image_rect_raw = np.zeros(g_frame_shape)

    self.pred_image = np.zeros(g_frame_shape)
    self.pred_image_raw = np.zeros(g_frame_shape)

    self.fps = 0

    self.callback_group = ReentrantCallbackGroup()
    self.model_path = os.path.join("./resource", "model.h5")
    print(self.model_path)
    self.model = tf.keras.models.load_model(self.model_path)
    # self.model.summary()
    self.rgb_codes = [
        [0, 0, 0],
        [70, 70, 70],
        [160, 160, 160]
        ]

    print("ros2 topic subscriber setting...", end="")
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

    self.cv_bridge = CvBridge()

    print("done")

    # Thread callback
    print("Treading start")
    self.flag_thread_unet_process = False
    self.thread_unet_process = threading.Thread(target=self.thread_unet_process_callback)
    self.thread_display = threading.Thread(target=self.thread_display_callback)
    self.thread_unet_process.start()
    self.thread_display.start()

  def grayscale_to_rgb(mask, rgb_codes):
    '''
    Custom Function for gray scale to rgb
    - not used
    '''
    h, w = mask.shape[0], mask.shape[1]
    mask = mask.astype(np.int32)
    output = []

    for i, pixel in enumerate(mask.flatten()):
        output.append(rgb_codes[pixel])

    output = np.reshape(output, (h, w, 3))
    return output

  def color_camera_info_callback(self, data):
    '''
    ROS
    Camera Info callback
    '''
    return

  def color_image_rect_raw_callback(self, data):
    '''
    ROS
    Get RGB frame
    '''
    # self.get_logger().info("Receiving RGB frame")
    self.rgb_frame = self.cv_bridge.imgmsg_to_cv2(data, 'bgr8')
    if self.rgb_frame.shape != g_frame_shape:
      self.rgb_frame = np.resize(self.rgb_frame, g_frame_shape)
    self.image_rect_raw = self.rgb_frame

    return

  def depth_camera_info_callback(self, data):
    return

  def depth_image_rect_raw_callback(self, data):
    '''
    ROS
    Get Depth frame
    '''
    self.depth_image_rect_raw = self.cv_bridge.imgmsg_to_cv2(data, desired_encoding='passthrough')
    return

  def imu_callback(self, data):
    return

  def thread_unet_process_callback(self):
    print('[UNET PROCESS THREAD] START')
    self.flag_thread_unet_process = True
    while True:
      strart_time = time.time()
      temp_rgb_frame = self.image_rect_raw

      rgb_frame = self.image_rect_raw
      rgb_frame = rgb_frame/255.0
      rgb_frame = np.expand_dims(rgb_frame, axis=0)
      rgb_frame = rgb_frame.astype(np.float32)

      pred = self.model.predict(rgb_frame)[0]    # [0] means : [1, w, h, rgb] -> [w,h,rgb]
      pred = np.argmax(pred, axis=-1)
      pred = pred.astype(np.int32)
      pred = pred*255./2

      pred_rgb = np.dstack((pred,)*3).astype(np.uint8)
      pred_rgb[:,:,1:3] = 0 # Blue (BRG)

      '''
      Both pred_image & pred_image_raw have to save at the same moment for imshow match
      '''
      self.pred_image = pred_rgb
      self.pred_image_raw = temp_rgb_frame

      # input_pred_image = np.concatenate((self.pred_image_raw, pred_rgb), axis=1)
      # combined_image = cv2.addWeighted(image_rect_raw, 0.01, pred_rgb, 0.90, 0, dtype = cv2.CV_32F)

      end_time = time.time()
      self.fps = 1 / (end_time - strart_time)


  def thread_display_callback(self):
    alpha = 0.5
    print('[DISPLAY THREAD] START')

    while True:
      try:
        while self.flag_thread_unet_process:
          depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(self.depth_image_rect_raw, alpha=0.5),
                                            cv2.COLORMAP_JET)
          bw_or_image = cv2.bitwise_or(self.pred_image_raw, self.pred_image)
          input_pred_image = np.concatenate((self.pred_image_raw, self.pred_image,bw_or_image), axis=0)

          fps_str = f'FPS = {self.fps:.2f}'

          cv2.putText(input_pred_image,
                      'image_rect_raw',
                      (10,30),
                      cv2.FONT_HERSHEY_SIMPLEX,
                      0.5,
                      (0, 255, 0),
                      1)
          cv2.putText(input_pred_image,
                      'predict',
                      (10,30+g_frame_shape[0]),
                      cv2.FONT_HERSHEY_SIMPLEX,
                      0.5,
                      (0, 255, 0),
                      1)
          cv2.putText(input_pred_image,
                      'synthesis',
                      (10,30+2*g_frame_shape[0]),
                      cv2.FONT_HERSHEY_SIMPLEX,
                      0.5,
                      (0, 255, 0),
                      1)
          cv2.putText(input_pred_image,
                      fps_str,
                      (10,30+30),
                      cv2.FONT_HERSHEY_SIMPLEX,
                      0.5,
                      (0, 0, 255),
                      1)

          # cv2.imshow('combined', combined_image)
          cv2.imshow('prediction', input_pred_image)
          # cv2.imshow('prediction2', bw_or_image)
          cv2.imshow('depth', depth_colormap)
          if cv2.waitKey(1) == ord('q'):
            break

      except Exception as e:
        self.get_logger().error('(DISPLAY THREAD) Error processing depth image: %s' % str(e))
        # break
    return

def main(args=None):
  rclpy.init(args=args)
  node = UNetProcessor()
  try:
    rclpy.spin(node)
  except KeyboardInterrupt:
    node.get_logger().info('Keyboard Interrupt (SIGINT)')
  finally:
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
  main()
