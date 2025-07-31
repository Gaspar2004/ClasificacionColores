
from essentials.waypoint import *
from config import *
from essentials.control import *
ROBOT_IP = "192.168.0.2"  # Cambiá esto por la IP real
PORT = 30002  # Puerto de URScript
STEP = 0.1

def prender_cinta3():
    script = f"""
    set_digital_out(3, True)
    """
    send_urscript(script)

def prender_cinta2():
    script = f"""
    set_digital_out(2, True)
    """
    send_urscript(script)


def apagar_cinta3():
    script = f"""
    set_digital_out(3, False)
    """
    send_urscript(script)

def apagar_cinta2():
    script = f"""
    set_digital_out(2, False)
    """
    send_urscript(script)

def send_urscript(script):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ROBOT_IP, PORT))
        s.sendall(script.encode("utf8"))
        time.sleep(0.1)


def move_direction(dx=0, dy=0, dz=0):
    script = f"""
def move_relative():
    pose = get_actual_tcp_pose()
    pose[0] = pose[0] + {dx}
    pose[1] = pose[1] + {dy}
    pose[2] = pose[2] + {dz}
    movel(pose, a=0.5, v=0.2)
end
move_relative()
"""
    send_urscript(script)
def move_up():
    move_direction(dz=STEP)

def move_down():
    move_direction(dz=-STEP)




