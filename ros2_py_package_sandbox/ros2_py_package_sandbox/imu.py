import rclpy
import serial
from rclpy.node import Node
from sensor_msgs.msg import Imu


ARDUINO_PORT = "/dev/ttyACM0"

class ImuBridge(Node):
    def __init__(self):
        super().__init__("imu_bridge_node")
        self.publisher_ = self.create_publisher(Imu, "imu/data_raw", 10)
        self.ser = serial.Serial(ARDUINO_PORT, 38400, timeout=1)
        self.timer = self.create_timer(0.01, self.timer_callback)

    def timer_callback(self):
        if self.ser.in_waiting > 0:
            # print(self.ser.readline())
            line = self.ser.readline().decode("utf-8", errors="ignore").strip()
            data = line.split(",")

            if len(data) == 6:
                try:
                    msg = Imu()
                    msg.header.stamp = self.get_clock().now().to_msg()
                    msg.header.frame_id = "imu_link"

                    # Convert raw to m/s^2 (assuming +/- 2g range)
                    msg.linear_acceleration.x = float(data[0]) * (9.806 / 16384.0)
                    msg.linear_acceleration.y = float(data[1]) * (9.806 / 16384.0)
                    msg.linear_acceleration.z = float(data[2]) * (9.806 / 16384.0)

                    # Convert raw to rad/s (assuming +/- 250 deg/s range)
                    msg.angular_velocity.x = float(data[3]) * (3.14159 / 180.0 / 131.0)
                    msg.angular_velocity.y = float(data[4]) * (3.14159 / 180.0 / 131.0)
                    msg.angular_velocity.z = float(data[5]) * (3.14159 / 180.0 / 131.0)

                    # Inside your timer_callback where you create the msg
                    msg.orientation_covariance = [0.0] * 9
                    msg.angular_velocity_covariance = [0.0] * 9
                    msg.linear_acceleration_covariance = [0.0] * 9

                    # Set the diagonals to a small non-zero number (e.g., 0.01)
                    msg.orientation_covariance[0] = 0.01
                    msg.orientation_covariance[4] = 0.01
                    msg.orientation_covariance[8] = 0.01
                    msg.angular_velocity_covariance[0] = 0.01
                    msg.angular_velocity_covariance[4] = 0.01
                    msg.angular_velocity_covariance[8] = 0.01
                    msg.linear_acceleration_covariance[0] = 0.01
                    msg.linear_acceleration_covariance[4] = 0.01
                    msg.linear_acceleration_covariance[8] = 0.01

                    self.publisher_.publish(msg)
                except Exception as e:
                    print(f"Failed to decode message: {line}")


def main(args=None):
    rclpy.init(args=args)
    node = ImuBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()





