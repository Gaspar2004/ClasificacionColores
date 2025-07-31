from essentials.settings import *

def estimate_move_time(target, typ, velocity, acceleration):
    if typ == 'l':
        distance = (target - globals['current_pos']).magnitude()
        # Si la distancia es cero, el tiempo es cero.
        if distance < 1e-6:
            return 0.0
        # 2. Calcular el tiempo de aceleración/desaceleración y la distancia recorrida en esas fases
        # t_accel = v / a
        # d_accel = 0.5 * a * t_accel^2 = 0.5 * a * (v/a)^2 = 0.5 * v^2 / a
        time_to_reach_max_vel = velocity / acceleration
        distance_during_accel = 0.5 * acceleration * time_to_reach_max_vel**2
        # El robot necesita acelerar y luego desacelerar, por lo tanto, 2 * distance_during_accel
        if distance <= 2 * distance_during_accel:
            # El movimiento es tan corto que el robot nunca alcanza la velocidad máxima.
            # Recorre toda la distancia acelerando y luego desacelerando.
            # Distancia = 0.5 * a * (t/2)^2 * 2 (ida y vuelta) = a * (t/2)^2
            # t/2 = sqrt(distancia / a)
            # t = 2 * sqrt(distancia / a)
            estimated_time = 2 * ((distance / acceleration) ** 0.5)
        else:
            # El robot acelera, mantiene la velocidad máxima, y luego desacelera.
            time_at_max_speed = (distance - (2 * distance_during_accel)) / velocity
            estimated_time = (2 * time_to_reach_max_vel) + time_at_max_speed
        # Añadir un pequeño colchón/margen de seguridad
        return estimated_time * EST_TIME_MARGEN
    else:
        return 0