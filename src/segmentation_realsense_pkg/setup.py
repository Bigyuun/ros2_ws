from setuptools import setup

package_name = 'segmentation_realsense_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    # packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bigyun',
    maintainer_email='bigyun9375@gmail.com',
    description='UNet using a realsense camera',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'realsense_subscriber = segmentation_realsense_pkg.realsense_subscriber:main',
            'process_node = segmentation_realsense_pkg.process_node:main'
        ],
    },
)
