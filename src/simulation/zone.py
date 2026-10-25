class Zone:
    """Airspace zone node representing a hub."""

    def __init__(self,
                 name: str,
                 x: int,
                 y: int,
                 type_z: str,
                 color: str,
                 max_drones: int):
        """Initialize zone attributes and capacity limits."""
        self.name = name
        self.x = x
        self.y = y
        self.type = type_z
        self.color = color
        self.max_drones = max_drones
