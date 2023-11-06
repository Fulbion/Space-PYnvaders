WIDTH: int = 800
HEIGHT: int = 600

BASE_ENEMY_COOLDOWN = 60

def clamp(x, min: float, max: float):
    if min <= x <= max: return x
    elif x < min: return min
    elif x > max: return max


class vec2:
    def __init__(self) -> None:
        self.x: float = 0.0
        self.y: float = 0.0

    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y