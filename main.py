#from OutputControl import *
#from CR3LIVE import *
from essentials.waypoint import *
from config import *
from essentials.control import *

ROBOT_IP = "192.168.0.2"  # Cambiá esto por la IP real
PORT = 30002  # Puerto de URScript

if __name__ == "__main__":
    movep(Approach)
    time.sleep(2)  # Espera para simular el agarre
