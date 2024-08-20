import rclpy
from rclpy.node import Node
from interface_pkg.msg import OnOff

class ACS(Node):
    def __init__(self):
        super().__init__("acs_node")
        self.onoff=1
        '''[onoff]
        default onoff = 1
        On = 1, Off = 0
        '''
        self.pub = self.create_publisher(OnOff, "ac_onoff", 10)

    def publish_data(self):
        msg = OnOff()
        onoff = input("Automatic Calibration (input on/off): ")
        
        if(onoff.lower()=='on'): 
            self.onoff = 1
        elif(onoff.lower()=='off'): 
            self.onoff = 0
        else: 
            print("[Error] input on/off only")
        
        msg.onoff = self.onoff
        self.pub.publish(msg)

def main():
    rclpy.init()
    
    acs=ACS()

    print("Automatic Calibration Activatied...")
    Num = 0
    while(rclpy.ok()):
        Num+=1
        print(f"[SPIN: {Num}]")
        try:
            acs.publish_data()
        except KeyboardInterrupt:
            acs.destroy_node()
            rclpy.shutdown()
        print("\n")
            

if __name__ == '__main__':
	main() 