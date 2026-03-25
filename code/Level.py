import pygame
import sys
import random

from code.Player import Player
from code.Dog import Dog
from code.Food import Food
from code.utils import load_image
from code.utils import load_sound
from code.utils import resource_path

class Level:

    def __init__(self, window):

        self.window = window

        self.player_img = load_image("assets/player_idle.png")
        self.player_img = pygame.transform.scale(self.player_img, (120, 120))

        self.player = Player(self.player_img, 100, 300)

        # cachorros
        self.dog_images = [
            load_image("assets/dog_idle_1.png"),
            load_image("assets/dog_idle_2.png"),
            load_image("assets/dog_idle_3.png"),
        ]

        self.dog_images = [
            pygame.transform.scale(img, (100, 100)) for img in self.dog_images
        ]

        # comidas boas
        self.good_food_imgs = [
            load_image("assets/cachorro_quente.png").convert_alpha(),
            load_image("assets/hamburguer.png").convert_alpha(),
            load_image("assets/pizza.png").convert_alpha(),
        ]

        # comidas ruins
        self.bad_food_imgs = [
            load_image("assets/brocolis.png").convert_alpha(),
            load_image("assets/fedor.png").convert_alpha(),
            load_image("assets/peixe_morto.png").convert_alpha(),
        ]

        self.good_food_imgs = [
            pygame.transform.scale(img, (40, 40)) for img in self.good_food_imgs
        ]

        self.bad_food_imgs = [
            pygame.transform.scale(img, (30, 30)) for img in self.bad_food_imgs
        ]

        # background
        self.bg_img = load_image("assets/background.png")
        self.bg_img = pygame.transform.scale(self.bg_img,(800,600))

        self.font = pygame.font.SysFont("Arial",25)

        # efeitos sonoros
        self.bark_sound = load_sound("assets/bark.wav")
        self.good_sound = load_sound("assets/good.wav")
        self.bad_sound = load_sound("assets/bad.wav")
        self.win_sound = load_sound("assets/win.wav")
        self.gameover_sound = load_sound("assets/gameover.wav")
        self.throw_sound = load_sound("assets/throw.wav")


        # volume
        self.bark_sound.set_volume(0.5)
        self.good_sound.set_volume(0.4)
        self.bad_sound.set_volume(0.5)
        self.win_sound.set_volume(1.3)
        self.gameover_sound.set_volume(0.8)
        self.throw_sound = load_sound("assets/throw.wav")

    def run(self):

        clock = pygame.time.Clock()

        #  música do jogo
        pygame.mixer.music.load(resource_path("assets/game_music.mp3"))
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        player = Player(self.player_img,100,300)

        dogs = []
        foods = []
        next_food_img, next_food_value = self.get_random_food()

        preview_img = pygame.transform.scale(next_food_img, (20, 20))

        score = 0

        floating_texts = []

        spawn_timer = 0
        spawn_delay = 90

        time_limit = 30
        start_time = pygame.time.get_ticks()

        bg_x = 0
        bg_speed = 2


        while True:

            clock.tick(60)

            self.window.fill((0, 0, 0))

            elapsed = (pygame.time.get_ticks() - start_time) / 1000
            time_left = int(time_limit - elapsed)


            spawn_timer += 1

            if spawn_timer >= spawn_delay:

                dog_img = random.choice(self.dog_images)

                dog = Dog(
                    dog_img,
                    820,
                    random.randint(50, 550)
                )

                dogs.append(dog)

                spawn_timer = 0


            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:
                        self.throw_sound.play()  # som do arremesso

                        food = Food(
                            next_food_img,
                            player.rect.right + 20,
                            player.rect.centery - 10,
                            next_food_value
                        )

                        foods.append(food)

                        # gera próxima comida
                        next_food_img, next_food_value = self.get_random_food()
                        preview_img = pygame.transform.scale(next_food_img, (20, 20))


            player.move()

            for dog in dogs:
                dog.move()

            for dog in dogs[:]:
                if dog.rect.colliderect(player.rect):
                    score -= 5
                    score = max(0, score)
                    self.bark_sound.play()

                    floating_texts.append({
                        "text": "-5",
                        "x": player.rect.centerx,
                        "y": player.rect.top,
                        "timer": 30
                    })

                    dogs.remove(dog)

            for food in foods:
                food.move()


            for dog in dogs[:]:

                if dog.rect.right < 0:
                    dogs.remove(dog)

            for food in foods[:]:
                for dog in dogs[:]:

                    if food.rect.colliderect(dog.rect):

                        # toca som
                        if food.value > 0:
                            self.good_sound.play()
                        else:
                            self.bad_sound.play()

                        # pontuação
                        score += food.value
                        score = max(0, score)

                        # texto flutuante
                        floating_texts.append({
                            "text": f"{food.value:+}",
                            "x": dog.rect.centerx,
                            "y": dog.rect.centery,
                            "timer": 30
                        })

                        # remove objetos
                        foods.remove(food)
                        dogs.remove(dog)

                        break

            bg_x -= bg_speed

            if bg_x <= -800:
                bg_x = 0


            self.window.blit(self.bg_img,(bg_x,0))
            self.window.blit(self.bg_img,(bg_x+800,0))


            self.window.blit(player.surf,player.rect)

            # preview da comida na mão
            self.window.blit(
                preview_img,
                (player.rect.right - 40, player.rect.centery - 0)
            )

            for dog in dogs:
                self.window.blit(dog.surf,dog.rect)

            for food in foods:
                self.window.blit(food.surf,food.rect)

            # Score e tempo
            score_text = self.font.render(f"Score: {score}", True, (0, 0, 0))
            time_text = self.font.render(f"Time: {time_left}", True, (0, 0, 0))

            pygame.draw.rect(self.window, (200, 200, 200), (5, 5, 200, 40), border_radius=10)
            pygame.draw.rect(self.window, (200, 200, 200), (600, 5, 190, 40), border_radius=10)

            pygame.draw.rect(self.window, (150, 150, 150), (5, 5, 200, 40), 2, border_radius=10)
            pygame.draw.rect(self.window, (150, 150, 150), (600, 5, 190, 40), 2, border_radius=10)

            self.window.blit(score_text, (20, 12))
            self.window.blit(time_text, (620, 12))

            for ft in floating_texts[:]:

                color = (0, 200, 0) if "+" in ft["text"] else (200, 0, 0)

                text_surf = self.font.render(ft["text"], True, color)
                self.window.blit(text_surf, (ft["x"], ft["y"]))

                ft["y"] -= 1
                ft["timer"] -= 1

                if ft["timer"] <= 0:
                    floating_texts.remove(ft)

            pygame.display.update()

            if score >= 100:
                pygame.mixer.music.fadeout(500)
                self.win_sound.play()
                self.show_message("YOU WIN!")
                return

            if score <= -50:
                pygame.mixer.music.fadeout(500)
                self.gameover_sound.play()
                self.show_message("GAME OVER")
                return

            if time_left <= 0:
                pygame.mixer.music.fadeout(500)
                self.gameover_sound.play()
                self.show_message("GAME OVER")
                return

    def show_message(self, text):

        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.window.blit(overlay, (0, 0))

        big_font = pygame.font.SysFont("Courier New", 60)
        if "WIN" in text:
            color = (0, 200, 0)  # verde
        else:
            color = (200, 0, 0)  # vermelho

        message = big_font.render(text, True, color)

        rect = message.get_rect(center=(400, 300))
        self.window.blit(message, rect)

        pygame.display.update()

        pygame.time.wait(2000)

    def get_random_food(self):
        if random.random() < 0.8:
            return random.choice(self.good_food_imgs), 10
        else:
            return random.choice(self.bad_food_imgs), -10