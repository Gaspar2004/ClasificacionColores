import socket
import time
from essentials.settings import *
from essentials.util import * 

def _send_urscript(script):
    # Crea una conexión al robot y envía el script URScript
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ROBOT_IP, ROBOT_PORT))
    s.send(script.encode('utf-8'))
    s.close()

def _send_dashboard_command(cmd):
    # Crea una conexión al puerto del dashboard y envía el comando
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ROBOT_IP, DASHBOARD_PORT))
        s.sendall((cmd + '\n').encode())
        time.sleep(0.5)
        response = s.recv(1024)
        #print(f"Dashboard response: {response.decode().strip()}")

def _set_as_current_position(waypoint):
    # Actualiza la posición actual del robot
    global globals
    globals['current_pos'] = waypoint

def _move(waypoint, typ, velocity=0.15, acceleration=1.2):
    # Convierte el waypoint a un script URScript y lo envía al robot
    x, y, z, rx, ry, rz = waypoint.get_components()
    script = f'move{typ}(p[{x},{y},{z},{rx},{ry},{rz}], a={acceleration}, v={velocity})\n'
    _send_urscript(script)
    # Estima el tiempo de movimiento y espera
    estimated_time = estimate_move_time(waypoint, typ, velocity, acceleration)
    time.sleep(estimated_time)
    _set_as_current_position(waypoint)

def movej(waypoint, velocity=MOVE_J_VELOCITY, acceleration=MOVE_J_ACCELERATION):
    return _move(waypoint, 'j', velocity, acceleration)

def movel(waypoint, velocity=MOVE_L_VELOCITY, acceleration=MOVE_L_ACCELERATION):
    return _move(waypoint, 'l', velocity, acceleration)

def movep(waypoint, velocity=MOVE_P_VELOCITY, acceleration=MOVE_P_ACCELERATION):
    return _move(waypoint, 'p', velocity, acceleration)

def open_gripper():
    # Carga y ejecuta el script para abrir la pinza
    _send_dashboard_command("load /programs/open_gripper.urp")
    _send_dashboard_command("play")
    time.sleep(5)

def close_gripper():
    # Carga y ejecuta el script para cerrar la pinza
    _send_dashboard_command("load /programs/close_gripper.urp")
    _send_dashboard_command("play")
    time.sleep(5)

def set_as_current_position(waypoint):
    return _set_as_current_position(waypoint)