import pygame

def scale_color(color: str, k: float) -> pygame.Color:
    base = pygame.Color(color)
    return pygame.Color(int(base.r * k), int(base.g * k), int(base.b * k))

def make_circle_glow(color: str, radius: int, intensity: float = 1.0) -> pygame.Surface:
    surface = pygame.Surface((radius * 2, radius * 2))
    for r in range(radius, 0, -1):
        k = intensity * (1 - r / radius) ** 2
        pygame.draw.circle(surface, scale_color(color, k), (radius, radius), r)
    return surface

def make_rect_glow(color: str, size: tuple[int, int], spread: int, intensity: float = 1.0) -> pygame.Surface:
    width, height = size
    surface = pygame.Surface((width + spread * 2, height + spread * 2))
    for i in range(spread, 0, -1):
        k = intensity * (1 - i / spread) ** 2
        rect = pygame.Rect(spread - i, spread - i, width + i * 2, height + i * 2)
        pygame.draw.rect(surface, scale_color(color, k), rect, border_radius=i + 6)
    return surface

def blit_glow(surface: pygame.Surface, glow: pygame.Surface, center) -> None:
    surface.blit(glow, glow.get_rect(center=center), special_flags=pygame.BLEND_ADD)

def render_glow_text(surface: pygame.Surface, font: pygame.font.Font, text: str, color: str, **rect_position) -> None:
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(**rect_position)

    padding = 16
    glow = pygame.Surface((rect.width + padding * 2, rect.height + padding * 2))
    glow.blit(font.render(text, True, color, "black"), (padding, padding))
    glow = pygame.transform.gaussian_blur(glow, 8)

    blit_glow(surface, glow, rect.center)
    surface.blit(text_surface, rect)
