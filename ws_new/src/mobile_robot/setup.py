from setuptools import setup

package_name = 'mobile_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    data_files=[
        ('share/ament_index/resource_index/ament_dependencies',
            ['resource/mobile_robot']),
        ('share/' + package_name, ['package.xml']),
    ],
    entry_points={
        'console_scripts': [
            'playback_node = mobile_robot.robot_nodes.playback_node:main',
        ],
    },
)
    