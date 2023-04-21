import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
import serial
import struct

class GarminPublisher(Node):

    def __init__(self):
        super().__init__('garmin_publisher')
        self.publisher_ = self.create_publisher(NavSatFix, 'garmin_gps_fix', 10)

        self.declare_parameter('serial_device', '/dev/ttyACM0')
        self.declare_parameter('baud_rate', 57600)
        self.declare_parameter('msg_period_sec', 0.4)
        self.serial_device = self.get_parameter('serial_device').get_parameter_value().string_value
        self.baud_rate = self.get_parameter('baud_rate').get_parameter_value().integer_value
        self.timer_period = self.get_parameter('msg_period_sec').get_parameter_value().double_value

        self.ser = serial.Serial(self.serial_device, self.baud_rate)
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

    def timer_callback(self):
        msg = NavSatFix()
        #self.get_logger().info('Entering callback')


        while (True):
            line = str(self.ser.readline())[2:]
            #self.get_logger().info('Reading: ' + line)
            if (line.startswith("$GPGGA") or line.startswith("$GNGGA")):
                break
        line = line.split(",")

        msg.header.stamp = self.get_clock().now().to_msg()

        lat = int(line[2][:2]) + (float(line[2][2:]) / 60)
        lat *= 1 if line[3] == "N" else -1
        msg.latitude = lat

        lon = int(line[4][:3]) + (float(line[4][3:]) / 60)
        lon *= 1 if line[5] == "E" else -1
        msg.longitude = lon

        msg.altitude = float(line[9])
        msg.status.service = 1 # GPS
        msg.status.status = 1 if line[6] == "1" else 0

        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: Garmin GPS Fix')


def main(args=None):
    rclpy.init(args=args)

    garmin_publisher = GarminPublisher()

    rclpy.spin(garmin_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    garmin_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
