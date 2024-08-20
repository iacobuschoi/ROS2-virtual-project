import rclpy
import traceback
from rclpy.node import Node
from interface_pkg.msg import Brightness
from interface_pkg.srv import DBI

class Screen(Node):
    def __init__(self):
        super().__init__("screen_node")
        self.out_brightness = 0.5
        self.dbi = 0.0
        self.timer = self.create_timer(1, self.publish_data)
        self.declare_parameter("screen_brightness", 0.5)
        
        self.sub = self.create_subscription(Brightness,"out_brightness",self.save_ob, 10)
        self.pub = self.create_publisher(Brightness, "screen_brightness", 10)

        self.client = self.create_client(DBI, "dbi")

        while not self.client.wait_for_service(0.1):
            self.get_logger().warning('The automatic calibration service not available.')

        self.timer = self.create_timer(0.5, self.publish_data)

    def save_ob(self, msg):
        self.out_brightness = msg.brightness
    
    def send_request(self):
        request = DBI.Request()
        request.ob = self.out_brightness
        request.sb = self.get_parameter("screen_brightness").get_parameter_value().double_value
        future = self.client.call_async(request)
        return future


    def calibration(self, dbi):    
        screen_brightness = self.get_parameter("screen_brightness").get_parameter_value().double_value
        dbi

        try:
            my_new_param = rclpy.parameter.Parameter(
                'screen_brightness',
                rclpy.Parameter.Type.DOUBLE,
                screen_brightness + dbi
            )
            all_new_parameters = [my_new_param]
            self.set_parameters(all_new_parameters)
            
            screen_brightness = self.get_parameter("screen_brightness").get_parameter_value().double_value

            print(f"[INFO] Resault New Screen Brightness: {screen_brightness}")

        except Exception:
            print("Exception !!!!")
            print(traceback.format_exc())
    
    def publish_data(self):
        self.calibration(self.dbi)
        msg = Brightness()
        msg.brightness = self.get_parameter("screen_brightness").get_parameter_value().double_value
        self.pub.publish(msg)
        print(f"[INFO] Publish Screen Brightness: {msg.brightness}")

def main(args=None):
    rclpy.init(args=args)

    screen = Screen()

    print("Screen Running...")

    Num = 0
    trigger = 1

    while(rclpy.ok()):
        
        Num+=1
        print(f"[SPIN: {Num}]")
        if trigger == 0:
            if future.done():
                response = future.result()
                screen.dbi = response.dbi
                trigger = 1
            else:    
                try:
                    rclpy.spin_once(screen)
                except KeyboardInterrupt:
                    screen.destroy_node()
                    rclpy.shutdown()          
        else:
            future = screen.send_request()
            trigger = 0
        print("\n")
        
if __name__ == '__main__':
	main() 