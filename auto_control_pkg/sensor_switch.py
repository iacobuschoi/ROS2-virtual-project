import rclpy
from rclpy.node import Node
from interface_pkg.msg import OnOff

class SS(Node):
    def __init__(self):
        super().__init__("sensor_switch_node")
        self.seneor_onoff = 1
        '''[sonoff]
        default onoff = 1
        On = 1, Off = 0
        '''
        self.pub = self.create_publisher(OnOff, "sensor_onoff",10)

    def publish_data(self):
        msg = OnOff()
        onoff = input("Brightness Sensor (input on/off): ")
        
        if(onoff.lower()=='on'): 
            self.sensor_onoff = 1
        elif(onoff.lower()=='off'): 
            self.sensor_onoff = 0
        else: 
            print("[Error] input on/off only")
        
        msg.onoff = self.sensor_onoff
        self.pub.publish(msg)

def main():
    rclpy.init()
    
    ss=SS()

    print("Sensor Switch Activatied...")
    Num = 0
    while(rclpy.ok()):
        Num+=1
        print(f"[SPIN: {Num}]")
        try:
            ss.publish_data()
        except KeyboardInterrupt:
            ss.destroy_node()
            rclpy.shutdown()
        print("\n")
            

if __name__ == '__main__':
	main() 