import pygame
import sys
import math

from code.utils import load_image
from code.utils import load_sound
from code.utils import resource_path

class Menu:
    def __init__(self, display):
        self.display = display

        # tamanho da tela
        self.width = self.display.get_width()
        self.height = self.display.get_height()

        # background
        self.bg = load_image("assets/menu_bg.png").convert()
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))

        # fontes
        self.title_font = pygame.font.SysFont("Courier New", 60, bold=True)
        self.base_font_size = 24  # 👈 base do efeito pulsar
        self.text_font = pygame.font.SysFont("Courier New", self.base_font_size)

        # controle do efeito
        self.scale_time = 0

        # controles
        self.title = self.title_font.render("FEED THE DOG", True, (255, 255, 255))

        self.controls = [
            "DIRECIONAIS - Se mover",
            "SPACE - Jogar comida",
            "Comida boa: +10 pts",
            "Comida ruim: -10 pts",
            "Mordida do dog: -5 pts",
            "",
            "Alimente os cachorros para somar pontos!",
        ]

        # som do select
        self.select_sound = load_sound("assets/select.wav")
        self.select_sound.set_volume(0.7)

    def run(self):
        clock = pygame.time.Clock()

        # música do menu
        pygame.mixer.music.load(resource_path("assets/menu_music.mp3"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        while True:
            state = self.events()

            if state == "start":
                pygame.mixer.music.stop()  # para a música ao iniciar o jogo
                return "start"

            self.update()
            self.draw()

            clock.tick(60)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.select_sound.play()
                    pygame.mixer.music.fadeout(300)
                    pygame.time.wait(200)
                    return "start"

    def update(self):
        # atualiza o tempo do efeito pulsar
        self.scale_time += 0.05

    def draw(self):
        # fundo
        self.display.blit(self.bg, (0, 0))

        # overlay escuro
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(80)
        overlay.fill((0, 0, 0))
        self.display.blit(overlay, (0, 0))

        # título
        self.display.blit(
            self.title,
            (self.width // 2 - self.title.get_width() // 2, 100)
        )

        # surface com transparência
        panel = pygame.Surface((560, 300))
        panel.set_alpha(170)
        panel.fill((50, 50, 50))

        # desenha na tela
        self.display.blit(panel, (self.width // 2 - 280, 170))

        # controles
        for i, line in enumerate(self.controls):
            text = self.text_font.render(line, True, (255, 255, 255))
            self.display.blit(
                text,
                (self.width // 2 - text.get_width() // 2, 180 + i * 40)
            )

        # select pulsando
        scale = 1 + 0.09 * math.sin(self.scale_time * 2)
        font_size = int(self.base_font_size * scale)

        pulse_font = pygame.font.SysFont("Arial", font_size)
        start_text = pulse_font.render(
            "Pressione ENTER para começar", True, (255, 255, 0)
        )

        rect = start_text.get_rect(center=(self.width // 2, 500))
        self.display.blit(start_text, rect)

        pygame.display.update()