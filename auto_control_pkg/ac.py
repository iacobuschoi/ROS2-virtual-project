import rclpy
from rclpy.node import Node
from interface_pkg.msg import OnOff
from interface_pkg.srv import DBI
from rclpy.callback_groups import ReentrantCallbackGroup
import traceback

class AC(Node):
    def __init__(self):
        super().__init__("ac_node")
        self.onoff = 1
        '''[ac_onoff]
        default onoff = 1
        On = 1, Off = 0
        '''
        self.dbi=0
        self.sub = self.create_subscription(OnOff, "ac_onoff", self.subf,10)

        self.callback_group = ReentrantCallbackGroup()

        self.ac_srv = self.create_service(
            DBI
            ,"dbi"
            ,self.calculate_dbi
            ,callback_group=self.callback_group
            )
    
    def subf(self, msg):
        self.onoff = msg.onoff
        onoffString=['OFF', 'ON']
        print("Automatic Calibration "+onoffString[self.onoff])

    def calculate_dbi(self, request, response):
        print("Dleta Brightness Index calaulating...")
        
        while(1):
            if self.onoff == 0:
                response.dbi = 0.0
                print("Automatic Calibrator is not working...")
                return response
            
            elif self.onoff == 1:
                ob = request.ob
                sb = request.sb
                if ob==0.0: response.dbi = 0.0
                else: response.dbi = (ob-sb)/2
                print(f"Send Response DBI: {response.dbi}")
                return response
            else:
                print("[Error] Automatic Calibrator On")
                self.onoff = 1

def main(args=None):
    rclpy.init(args=args)

    ac = AC()

    print("Automatic Calibrator Running...")
    Num = 0
    while(rclpy.ok()):
        Num+=1
        print(f"[SPIN: {Num}]")
        try:
            rclpy.spin_once(ac)
        except KeyboardInterrupt:
            ac.destroy_node()
            rclpy.shutdown()
        print("\n")
        
if __name__ == '__main__':
	main() 


        
        
        
