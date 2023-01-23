import time
import sys
sys.path.append(r'/home/frozaidi/IntroIIPiCarTA/picar-x')
from picarx_improved import Picarx      # noqa: E402


def drive(picarx, dir="forward", angle=0, sleep=5):
    """
    function to drive the PicarX forwards
    :param dir: Direction of movement, forwards or backwards
    :param angle: Angle of steering, from -40 to 40 degrees
    :param sleep: The amount of time to drive the car
    """
    picarx.set_dir_servo_angle(angle)
    if dir == "forward":
        picarx.forward(100)
        time.sleep(sleep)
        picarx.stop()
    elif dir == "backward":
        picarx.backward(100)
        time.sleep(sleep)
        picarx.stop()
    else:
        print("Not a valid direction. Try again.")


def parallel_parking(picarx, dir="left"):
    """
    function to perform a parallel parking maneuver for the PicarX
    :param dir: Side of parking, left or right
    """
    if dir == "left":
        picarx.set_dir_servo_angle(-35)
        picarx.backward(100)
        time.sleep(0.5)
        picarx.set_dir_servo_angle(35)
        time.sleep(1.0)
        picarx.set_dir_servo_angle(0)
        picarx.forward(100)
        time.sleep(0.1)
        picarx.stop()
    elif dir == "right":
        picarx.set_dir_servo_angle(35)
        picarx.backward(100)
        time.sleep(0.5)
        picarx.set_dir_servo_angle(-35)
        time.sleep(1.0)
        picarx.set_dir_servo_angle(0)
        picarx.forward(100)
        time.sleep(0.1)
        picarx.stop()
    else:
        print("Not a valid direction. Try again.")


def k_turn(picarx, dir="left"):
    """
    function to perform a k-turn maneuver for the PicarX
    :param dir: Direction of initial movement, left or right
    """
    if dir == "left":
        picarx.set_dir_servo_angle(-35)
        picarx.forward(100)
        time.sleep(1)
        picarx.set_dir_servo_angle(35)
        picarx.backward(100)
        time.sleep(1)
        picarx.set_dir_servo_angle(0)
        picarx.forward(100)
        time.sleep(1)
        picarx.stop()
    elif dir == "right":
        picarx.set_dir_servo_angle(35)
        picarx.forward(100)
        time.sleep(1)
        picarx.set_dir_servo_angle(-35)
        picarx.backward(100)
        time.sleep(1)
        picarx.set_dir_servo_angle(0)
        picarx.forward(100)
        time.sleep(1)
        picarx.stop()
    else:
        print("Not a valid direction. Try again.")


if __name__ == '__main__':
    px = Picarx()       # instantiate the PicarX class
    flag = False        # set a flag to stop the while loop
    while flag is False:
        # ask for input of type of maneuver, call the corresponding function
        maneuver = input("Select maneuver type [drive/parallel/kturn]: ")
        if maneuver == "drive":
            dir = input("Input direction [forward/backward]: ")
            angle = int(input("Input angle [-40,40]: "))
            sleep = int(input("Input duration of drive (seconds): "))
            drive(px, dir, angle, sleep)
        elif maneuver == "parallel":
            dir = input("Input direction [left/right]: ")
            parallel_parking(px, dir)
        elif maneuver == "kturn":
            dir = input("Input direction [left/right]: ")
            k_turn(px, dir)
        else:
            print("Invalid maneuver, try again, you absolute fool.")
        # at the end of the maneuver, ask user if they want to perform another
        continue_maneuver = input("Try another maneuver [y/n]? ")
        if continue_maneuver == "y":
            continue
        elif continue_maneuver == "n":
            flag = True
        else:
            print("Invalid response. Terminating program, you fool.")
            flag = True