import pygame
from pygame import Vector2
from game_object import GameObject
from neon import make_rect_glow, blit_glow

class Box(GameObject):
    FILL_COLOR = "#0d0221"

    def __init__(self, color: str, position: Vector2, width: float, height: float):
        super().__init__(color, position)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        self.glow = make_rect_glow(color, self.rect.size, 25, 0.6)

    def render(self, surface: pygame.Surface) -> None:
        blit_glow(surface, self.glow, self.rect.center)
        pygame.draw.rect(surface, self.FILL_COLOR, self.rect, border_radius=6)
        pygame.draw.rect(surface, self.color, self.rect, 2, border_radius=6)