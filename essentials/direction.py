class Direction:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"Direction(x={self.x}, y={self.y}, z={self.z})"
    
    def __add__(self, other):
        if isinstance(other, Direction):
            return Direction(
                self.x + other.x,
                self.y + other.y,
                self.z + other.z
            )
        return NotImplemented
    
    def __sub__(self, other):
        if isinstance(other, Direction):
            return Direction(
                self.x - other.x,
                self.y - other.y,
                self.z - other.z
            )
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Direction(
                self.x * other,
                self.y * other,
                self.z * other
            )
        elif isinstance(other, Direction):
            return Direction(
                self.x * other.x,
                self.y * other.y,
                self.z * other.z
            )
        return NotImplemented
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Direction(
                self.x / other,
                self.y / other,
                self.z / other
            )
        elif isinstance(other, Direction):
            return Direction(
                self.x / other.x if other.x != 0 else 0,
                self.y / other.y if other.y != 0 else 0,
                self.z / other.z if other.z != 0 else 0
            )
        return NotImplemented
    
    def magnitude(self):
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5
    
    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Direction(0, 0, 0)
        return self / mag