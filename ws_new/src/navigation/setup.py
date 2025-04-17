from setuptools import setup

package_name = 'navigation'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    entry_points={
        'console_scripts': [
            'nav_node = navigation.nav_node:main',
            'gps_path_follow = navigation.gps_path_follow:main',
            'waypoint_follow = navigation.waypoint_follow:main',
        ],
    },
)