import rclpy
from rclpy.node import Node
from interface_pkg.msg import OnOff
from interface_pkg.msg import Brightness

class Main(Node):
    def __init__(self):
        super().__init__("main_node")
        self.out_brightness = 0.5
        self.screen_brightness = 0.5
        self.sensor_onoff = 1
        self.ac_onoff = 1

        self.so_sub = self.create_subscription(OnOff,"sensor_onoff",self.so_subf,10)
        self.aco_sub = self.create_subscription(OnOff,"ac_onoff",self.aco_subf,10)
        self.ob_sub = self.create_subscription(Brightness,"out_brightness",self.ob_subf,10)
        self.sb_sub = self.create_subscription(Brightness,"screen_brightness",self.sb_subf,10)
    
    def so_subf(self,msg):
        self.sensor_onoff = msg.onoff

    def aco_subf(self,msg):
        self.ac_onoff = msg.onoff

    def ob_subf(self,msg):
        self.out_brightness = msg.brightness

    def sb_subf(self,msg):
        self.screen_brightness = msg.brightness

def main():
    rclpy.init()

    f = open("log.txt","w")
    main_node = Main()

    print("Main Running...")
    Num = 0
    while(rclpy.ok()):
        Num+=1
        print(f"[SPIN: {Num}]")
        try:
            rclpy.spin_once(main_node)
            print(f"[INFO] Brightness Sensor:     {main_node.sensor_onoff}")
            print(f"[INFO] Automatic Caliblation: {main_node.ac_onoff}")
            print(f"[INFO] Out Brghtness:         {main_node.out_brightness}")
            print(f"[INFO] Screen Brightness:     {main_node.screen_brightness}")
            f.write(f"{main_node.sensor_onoff} {main_node.ac_onoff} {main_node.out_brightness} {main_node.screen_brightness}\n")
            
        except KeyboardInterrupt:
            main_node.destroy_node()
            rclpy.shutdown()
        print("\n")
    f.close()
        
if __name__ == '__main__':
	main() 

