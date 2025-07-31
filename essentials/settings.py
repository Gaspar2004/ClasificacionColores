
ROBOT_IP = "192.168.0.2"
ROBOT_PORT = 30002
DASHBOARD_PORT = 29999

# Velocidades y aceleraciones por defecto para los movimientos

MOVE_J_VELOCITY = 0.4
MOVE_J_ACCELERATION = 1.2

MOVE_L_VELOCITY = 1.5
MOVE_L_ACCELERATION = 1.2

MOVE_P_VELOCITY = 0.15
MOVE_P_ACCELERATION = 0.1

EST_TIME_MARGEN = 1.2 # Margen de seguridad del para el tiempo estimado de movimiento


# Variables globales (no tocar)
globals = {
    'current_pos': None
}