#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
import RPi.GPIO as GPIO

tirette_chan = 38

class TiretteNode(Node):
    def __init__(self):
        super().__init__('tirette_node')
        self.publisher = self.create_publisher(Bool, 'tirette', 10)
        self.timer = self.create_timer(0.1, self.publish_tirette_value)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(tirette_chan, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def publish_tirette_value(self):
        tirette_value = GPIO.input(tirette_chan)
        msg = Bool()
        msg.data = bool(tirette_value)
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    tirette_node = TiretteNode()
    try:
        rclpy.spin(tirette_node)
    except KeyboardInterrupt:
        pass
    finally:
        tirette_node.destroy_node()
        GPIO.cleanup()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

