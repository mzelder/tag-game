import pygame
from pygame import Vector2
from player import Player
from box import Box

class Game:
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 48)

        self.player1 = Player("red", Vector2(self.SCREEN_WIDTH / 2 - 200, self.SCREEN_HEIGHT / 2))
        self.player2 = Player("blue", Vector2(self.SCREEN_WIDTH / 2 + 200, self.SCREEN_HEIGHT / 2))
        self.it = self.player1

        self.boxes = [
            Box("black", Vector2(self.SCREEN_WIDTH / 2 - 50, 250), 100, 100),
            Box("black", Vector2(self.SCREEN_WIDTH / 2 - 50, 650), 100, 100),
        ]

    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.save_positions()
            self.handle_input()
            self.check_box_collisions()
            self.check_tag()

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

    def check_box_collisions(self) -> None:
        if self.colides_with_box(self.player1): self.player1.restore_position()
        if self.colides_with_box(self.player2): self.player2.restore_position()

    def colides_with_box(self, player: Player) -> bool:
        return any(box.colide(player) for box in self.boxes)

    def check_tag(self) -> None:
        if self.player1.colide(self.player2):
            self.it.score += 1
            self.it = self.player2 if self.it is self.player1 else self.player1
            self.player1.restart_to_starting_position()
            self.player2.restart_to_starting_position()

    def render_screen(self) -> None:
        self.screen.fill("gray")
        for box in self.boxes:
            box.render(self.screen)
        self.player1.render(self.screen, self.it is self.player1)
        self.player2.render(self.screen, self.it is self.player2)

    def render_score(self) -> None:
        red_score = self.font.render(str(self.player1.score), True, self.player1.color)
        blue_score = self.font.render(str(self.player2.score), True, self.player2.color)
        self.screen.blit(red_score, red_score.get_rect(topleft=(20, 20)))
        self.screen.blit(blue_score, blue_score.get_rect(topright=(self.screen.get_width() - 20, 20)))
