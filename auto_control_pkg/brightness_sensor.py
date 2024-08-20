import rclpy
from rclpy.node import Node
from interface_pkg.msg import OnOff
from interface_pkg.msg import Brightness

class BS(Node):
    def __init__(self):
        super().__init__("brightness_sensor_node")
        self.onoff = 1 
        '''[seneor_onoff]
        default onoff = 1
        On = 1, Off = 0
        '''
        self.declare_parameter("out_brightness",0.5)
        '''[out_brightness]
        default out_brightness = 0.5
        '''
        self.timer = self.create_timer(0.5,self.publish_data)
        self.sub = self.create_subscription(OnOff, "sensor_onoff",self.sensor_switch_onoff, 10)
        self.pub = self.create_publisher(Brightness, "out_brightness",10)

    def sensor_switch_onoff(self, onoff_msg):
        self.onoff = onoff_msg.onoff
        onoffString=['OFF', 'ON']
        print("Brightness sensor "+onoffString[self.onoff])

    def publish_data(self):
        msg = Brightness()
        out_brightness=self.get_parameter("out_brightness").get_parameter_value().double_value
        if(self.onoff==0):out_brightness=0.0
        msg.brightness = out_brightness
        self.pub.publish(msg)
        if(self.onoff==1): print(f"publish success... out_brightness = {out_brightness}")
        else: print("sensor is no working")
def main():
    rclpy.init()

    bs=BS()

    print("Brightness Sensor Running...")
    Num = 0
    while(rclpy.ok()):
        Num+=1
        print(f"[SPIN: {Num}]")
        try:
            rclpy.spin_once(bs)
        except KeyboardInterrupt:
            bs.destroy_node()
            rclpy.shutdown()
        print("\n")
        
if __name__ == '__main__':
	main() 