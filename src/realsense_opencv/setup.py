from setuptools import setup

package_name = 'realsense_opencv'

setup(
    name=package_name,
    version='0.6.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bigyun',
    maintainer_email='bigyun9375@gmail.com',
    description='ROS2 rclpy Intel(R) RealSense camera custom package',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'realsense_subscriber = realsense_opencv.realsense_subscriber:main'
        ],
    },
)
