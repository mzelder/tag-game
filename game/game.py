import pygame
from pygame import Vector2
from game.player import Player
from game.box import Box
from game.neon import render_glow_text
from game.background import make_background

class Game:
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("consolas", 48, bold=True)
        self.background = make_background(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        self.player1 = Player("#ff2a6d", Vector2(self.SCREEN_WIDTH / 2 - 200, self.SCREEN_HEIGHT / 2))
        self.player2 = Player("#05d9e8", Vector2(self.SCREEN_WIDTH / 2 + 200, self.SCREEN_HEIGHT / 2))
        self.it = self.player1

        self.boxes = [
            Box("#b026ff", Vector2(self.SCREEN_WIDTH / 2 - 50, 250), 100, 100),
            Box("#b026ff", Vector2(self.SCREEN_WIDTH / 2 - 50, 650), 100, 100),
        ]

    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.save_positions()
            self.handle_input()
            self.check_collisions()
            self.check_tag()
            self.update_trails()

            self.render_screen()
            self.render_score()
            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def save_positions(self) -> None:
        self.player1.save_position()
        self.player2.save_position()

    def handle_input(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.player1.move_up()
        if keys[pygame.K_s]: self.player1.move_down()
        if keys[pygame.K_a]: self.player1.move_left()
        if keys[pygame.K_d]: self.player1.move_right()

        if keys[pygame.K_UP]: self.player2.move_up()
        if keys[pygame.K_DOWN]: self.player2.move_down()
        if keys[pygame.K_LEFT]: self.player2.move_left()
        if keys[pygame.K_RIGHT]: self.player2.move_right()

    def check_collisions(self) -> None:
        #box collisions
        if self.colides_with_box(self.player1): self.player1.restore_position()
        if self.colides_with_box(self.player2): self.player2.restore_position()

        #window boundary collisions
        if self.is_out_of_bounds(self.player1): self.player1.restore_position()
        if self.is_out_of_bounds(self.player2): self.player2.restore_position()

    def colides_with_box(self, player: Player) -> bool:
        return any(player.colide(box) for box in self.boxes)

    def is_out_of_bounds(self, player: Player) -> bool:
        return not player.is_inside(self.screen.get_rect())

    def check_tag(self) -> None:
        if self.player1.colide(self.player2):
            self.it.score += 1
            self.it = self.player2 if self.it is self.player1 else self.player1
            self.player1.restart_to_starting_position()
            self.player2.restart_to_starting_position()

    def update_trails(self) -> None:
        self.player1.update_trail()
        self.player2.update_trail()

    def render_screen(self) -> None:
        self.screen.blit(self.background, (0, 0))
        for box in self.boxes:
            box.render(self.screen)
        self.player1.render(self.screen, self.it is self.player1)
        self.player2.render(self.screen, self.it is self.player2)

    def render_score(self) -> None:
        render_glow_text(self.screen, self.font, f"{self.player1.score:02}", self.player1.color, topleft=(30, 25))
        render_glow_text(self.screen, self.font, f"{self.player2.score:02}", self.player2.color, topright=(self.screen.get_width() - 30, 25))
