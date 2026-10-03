import pygame
from pygame import Vector2
from game_object import GameObject
from player import Player

class Box(GameObject):
    def __init__(self, color: str, position: Vector2, width: float, height: float):
        super().__init__(color, position)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)

    def render(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)

    def colide(self, player: Player) -> bool:
        closest_x = max(self.rect.left, min(player.position.x, self.rect.right))
        closest_y = max(self.rect.top, min(player.position.y, self.rect.bottom))
        return player.position.distance_to(Vector2(closest_x, closest_y)) <= player.radius
