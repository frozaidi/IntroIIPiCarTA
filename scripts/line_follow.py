
import time
import sys
sys.path.append(r'/home/frozaidi/IntroIIPiCarTA/picarx')
from picarx_improved import Picarx      # noqa: E402
from interpreter import Interpreter     # noqa: E402
from sensor import GrayscaleSensor      # noqa: E402
from controller import Controller       # noqa: E402


if __name__ == '__main__':
    """
    This script imports all helper functions and follows a line while moving
    forwards at a constant speed
    """
    px = Picarx()
    scale = int(input("Enter scale: "))
    polarity = int(input("Enter polarity:"))
    con = Controller(px, scale)
    sens = GrayscaleSensor()
    inter = Interpreter(0.0, polarity)

    while True:
        list = sens.get_grayscale_data()
        rel_dir = inter.edge_detect(list)
        angle = con.line_follow(rel_dir)
        print("Steering angle: "+str(angle))
        px.forward(40)
        time.sleep(0.1)
