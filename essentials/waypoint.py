from essentials.direction import Direction
import math

class Waypoint:
    def __init__(self, x=0, y=0, z=0, rx=0, ry=0, rz=0):
        self.x = x
        self.y = y
        self.z = z
        self.rx = rx
        self.ry = ry
        self.rz = rz

    def __str__(self):
        return f"Waypoint(x={self.x}, y={self.y}, z={self.z}, rx={self.rx}, ry={self.ry}, rz={self.rz})"
    
    ## Suma entre dos waypoints
    def __add__(self, other):
        if isinstance(other, Waypoint):
            return Waypoint(
                self.x + other.x,
                self.y + other.y,
                self.z + other.z,
                self.rx + other.rx,
                self.ry + other.ry,
                self.rz + other.rz
            )
        elif isinstance(other, Direction):
            return Waypoint(
                self.x + other.x,
                self.y + other.y,
                self.z + other.z,
                self.rx,
                self.ry,
                self.rz
            )
        return NotImplemented
    
    ## Resta entre dos waypoints
    def __sub__(self, other):
        if isinstance(other, Waypoint):
            return Waypoint(
                self.x - other.x,
                self.y - other.y,
                self.z - other.z,
                self.rx - other.rx,
                self.ry - other.ry,
                self.rz - other.rz
            )
        elif isinstance(other, Direction):
            return Waypoint(
                self.x - other.x,
                self.y - other.y,
                self.z - other.z,
                self.rx,
                self.ry,
                self.rz
            )
        return NotImplemented

    ## Multiplicación de un waypoint por un escalar, waypoint o direction
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Waypoint(
                self.x * other,
                self.y * other,
                self.z * other,
                self.rx,
                self.ry,
                self.rz
            )
        elif isinstance(other, Waypoint):
            # Emulate CFrame * CFrame (combine positions and rotations)
            return Waypoint(
                self.x + other.x,
                self.y + other.y,
                self.z + other.z,
                self.rx + other.rx,
                self.ry + other.ry,
                self.rz + other.rz
            )
        elif isinstance(other, Direction):
            # Rotation matrices
            cos_rx, sin_rx = math.cos(self.rx), math.sin(self.rx)
            cos_ry, sin_ry = math.cos(self.ry), math.sin(self.ry)
            cos_rz, sin_rz = math.cos(self.rz), math.sin(self.rz)
            # Roll (X axis)
            x1 = other.x
            y1 = other.y * cos_rx - other.z * sin_rx
            z1 = other.y * sin_rx + other.z * cos_rx
            # Pitch (Y axis)
            x2 = x1 * cos_ry + z1 * sin_ry
            y2 = y1
            z2 = -x1 * sin_ry + z1 * cos_ry
            # Yaw (Z axis)
            dx = x2 * cos_rz - y2 * sin_rz
            dy = x2 * sin_rz + y2 * cos_rz
            dz = z2
            return Waypoint(
                self.x + dx,
                self.y + dy,
                self.z + dz,
                self.rx,
                self.ry,
                self.rz
            )
        return NotImplemented

    ## División de un waypoint por un escalar
    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)) and scalar != 0:
            return Waypoint(
                self.x / scalar,
                self.y / scalar,
                self.z / scalar,
                self.rx,
                self.ry,
                self.rz
            )
        return NotImplemented

    def get_angles(self):
        return self.rx, self.ry, self.rz

    def get_components(self):
        return self.x, self.y, self.z, self.rx, self.ry, self.rz
    
    def magnitude(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5