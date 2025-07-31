import socket
import time
# Dirección IP del robot y puerto URScript
ROBOT_IP = "192.168.0.2"  # Cambiá esto por la IP real
PORT = 30002  # Puerto de URScript

# Script URScript a enviar
script = """
def control_digital_output():
    set_digital_out(3, True)
    sleep(2.0)
    set_digital_out(3, False)
end

control_digital_output()
"""

# Enviar script al robot
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ROBOT_IP, PORT))
sock.send(script.encode('utf8'))
time.sleep(1)
sock.close()
