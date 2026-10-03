import pygame
from pygame import Vector2

class GameObject:
    def __init__(self, color: str, position: Vector2):
        self.color = color
        self.position = Vector2(position)

    def render(self, surface: pygame.Surface) -> None:
        raise NotImplementedError

    def colide(self, other: GameObject) -> bool:
        raise NotImplementedError
