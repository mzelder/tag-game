import pygame 
from pygame import Vector2

class Player:
    def __init__(self, color: str, position: Vector2):
        self.speed = 5
        self.width =  3
        self.radius = 10
        self.color = color
        self.position = Vector2(position)
        self.starting_position = Vector2(position)
        self.score = 0

    def render(self, surface: pygame.Surface, is_it: bool = False)-> None:
        if is_it:
            pygame.draw.circle(surface, self.color, self.position, self.radius)
            pygame.draw.circle(surface, "black", self.position, self.radius + 6, 2)
        else:
            pygame.draw.circle(surface, self.color, self.position, self.radius, self.width)

    def colide(self, other: Player) -> bool:
        return self.position.distance_to(other.position) <= self.radius + other.radius

    def restart_to_starting_position(self) -> None:
        self.position = Vector2(self.starting_position)

    def move_up(self) -> None:
        self.position.y -= self.speed

    def move_down(self) -> None:
        self.position.y += self.speed

    def move_left(self) -> None:
        self.position.x -= self.speed

    def move_right(self) -> None:
        self.position.x += self.speed