import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/thomas/MobileRobot/ws_new/install/nav2_loopback_sim'
