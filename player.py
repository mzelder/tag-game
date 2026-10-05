import math
import pygame
from box import Box
from pygame import Vector2
from game_object import GameObject
from neon import make_circle_glow, blit_glow, scale_color
from collections import deque

class Player(GameObject):
    TRAIL_LENGTH = 14

    def __init__(self, color: str, position: Vector2):
        super().__init__(color, position)
        self.speed = 5
        self.width =  3
        self.radius = 10
        self.starting_position = Vector2(position)
        self.previous_position = Vector2(position)
        self.score = 0
        self.trail = deque(maxlen=self.TRAIL_LENGTH)
        self.glow = make_circle_glow(color, 35, 0.5)
        self.it_glow = make_circle_glow(color, 55, 0.9)

    def render(self, surface: pygame.Surface, is_it: bool = False)-> None:
        self.render_trail(surface)
        if is_it:
            pulse = (math.sin(pygame.time.get_ticks() / 120) + 1) / 2
            blit_glow(surface, self.it_glow, self.position)
            pygame.draw.circle(surface, self.color, self.position, self.radius)
            pygame.draw.circle(surface, "white", self.position, self.radius // 2)
            pygame.draw.circle(surface, self.color, self.position, self.radius + 6 + pulse * 4, 2)
        else:
            blit_glow(surface, self.glow, self.position)
            pygame.draw.circle(surface, self.color, self.position, self.radius, self.width)

    def render_trail(self, surface: pygame.Surface) -> None:
        for i, position in enumerate(self.trail):
            k = (i + 1) / self.TRAIL_LENGTH
            pygame.draw.circle(surface, scale_color(self.color, k * 0.6), position, self.radius * k)

    def update_trail(self) -> None:
        self.trail.append(Vector2(self.position))

    def colide(self, other: GameObject) -> bool:
        if isinstance(other, Player):
            return self.position.distance_to(other.position) <= self.radius + other.radius
        if isinstance(other, Box):
            closest_x = max(other.rect.left, min(self.position.x, other.rect.right))
            closest_y = max(other.rect.top, min(self.position.y, other.rect.bottom))
            return self.position.distance_to(Vector2(closest_x, closest_y)) <= self.radius
        raise TypeError(f"can't collide Player with {type(other).__name__}")

    def is_inside(self, rect: pygame.Rect) -> bool:
        return (rect.left + self.radius <= self.position.x <= rect.right - self.radius and
                rect.top + self.radius <= self.position.y <= rect.bottom - self.radius)

    def restart_to_starting_position(self) -> None:
        self.position = Vector2(self.starting_position)
        self.trail.clear()

    def save_position(self) -> None:
        self.previous_position = Vector2(self.position)

    def restore_position(self) -> None:
        self.position = Vector2(self.previous_position)

    def move_up(self) -> None:
        self.position.y -= self.speed

    def move_down(self) -> None:
        self.position.y += self.speed

    def move_left(self) -> None:
        self.position.x -= self.speed

    def move_right(self) -> None:
        self.position.x += self.speed
