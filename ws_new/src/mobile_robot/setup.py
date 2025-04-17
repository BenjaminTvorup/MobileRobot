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
            # New node entry point for your navigation file
            'navigation = navigation.navigation:main',
        ],
    },
)
    