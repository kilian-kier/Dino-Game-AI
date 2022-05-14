import pygame
import random
import os
import config as config
from dino import Dino
from cactus import Cactus, cactus_images
from ground import Ground
from ai import play_ai, train_ai


def draw(mode, ground, dinos, cacti, score, alive):
    ground.move()
    ground.draw()
    for c in cacti:
        c.move()
        c.draw()
    for dino in dinos:
        dino.move()
        dino.draw()
    score_text = config.STAT_FONT.render("Score: " + str(score), True, (180, 180, 180))
    config.WIN.blit(score_text, (config.WIN_WIDTH - score_text.get_width() - 15, 10))
    if mode != 1:
        high_score_text = config.STAT_FONT.render(
            "High-Score: " + str(config.HIGH_SCORE), True, (180, 180, 180))
        config.WIN.blit(high_score_text, (config.WIN_WIDTH - score_text.get_width() -
                                          high_score_text.get_width() - 30, 10))
    if mode == 1:
        gen_text = config.STAT_FONT.render("Gen: " + str(config.GEN), True, (180, 180, 180))
        config.WIN.blit(gen_text, (15, 10))
        alive_text = config.STAT_FONT.render(
            "Alive: " + str(alive), True, (180, 180, 180))
        config.WIN.blit(alive_text, (15, gen_text.get_height() + 20))
    pygame.display.flip()
    pygame.display.update()


def update_cacti(cacti):
    rem = []
    for c in cacti:
        if c.x + c.img.get_width() < 0:
            rem.append(c)
    for r in rem:
        cacti.remove(r)

    if cacti[-1].x < config.WIN_WIDTH - cactus_images[0].get_width():
        cacti.append(Cactus(cacti[-1].x + random.randint(200, 800)))


def real_player():
    dino = Dino()
    ground = Ground()
    cacti = [Cactus(config.WIN_WIDTH + random.randint(0, 250))]

    clock = pygame.time.Clock()
    run = True

    score = 0
    ticks = 0

    while run:
        config.WIN.fill((0, 0, 0))
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_SPACE:
                    dino.jump()

        for cactus in cacti:
            if cactus.collide(dino):
                run = False

        if run:
            draw(0, ground, [dino], cacti, score, 0)
            update_cacti(cacti)
            ticks += 1
            if ticks % (config.SPEED * 2) == 0:
                score += 1
    if config.HIGH_SCORE < score:
        config.HIGH_SCORE = score


def draw_menu_options(text, y):
    config.WIN.blit(text, (config.WIN_WIDTH / 2 - text.get_width() / 2, y + 10))
    pygame.draw.rect(config.WIN, (180, 180, 180), (config.WIN_WIDTH / 2 - 50, y, 100, 40), 2, 5)


def start():
    real_y = config.WIN_HEIGHT / 5 * 1
    real_text = config.STAT_FONT.render("Play", True, (180, 180, 180))

    train_y = config.WIN_HEIGHT / 5 * 2
    train_text = config.STAT_FONT.render("Train AI", True, (180, 180, 180))

    ai_y = config.WIN_HEIGHT / 5 * 3
    play_ai_text = config.STAT_FONT.render("Play AI", True, (180, 180, 180))

    reset_y = config.WIN_HEIGHT / 5 * 4
    reset_text = config.STAT_FONT.render("Reset", True, (180, 180, 180))

    clock = pygame.time.Clock()

    gen_input = "10"

    while True:
        gens = None
        mouse = pygame.mouse.get_pos()
        if gen_input == "":
            gen_input = "0"
        try:
            gens = int(gen_input)
        except ValueError:
            print("Invalid input")
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if config.WIN_WIDTH / 2 - 50 <= mouse[0] <= config.WIN_WIDTH / 2 + 50:
                    if real_y <= mouse[1] <= real_y + 40:
                        real_player()
                    elif train_y <= mouse[1] <= train_y + 40:
                        train_ai(gens)
                    elif ai_y <= mouse[1] <= ai_y + 40:
                        play_ai()
                    elif reset_y <= mouse[1] <= reset_y + 40:
                        config.HIGH_SCORE = 0
                        try:
                            open("ai.pkl", "rb")
                        except FileNotFoundError:
                            pass
                        else:
                            os.remove("ai.pkl")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_BACKSPACE:
                    gen_input = gen_input[:-1]
                elif "0" <= event.unicode <= "9":
                    gen_input += event.unicode

        config.WIN.fill((0, 0, 0))
        draw_menu_options(real_text, real_y)
        draw_menu_options(train_text, train_y)
        gen_text = config.STAT_FONT.render(str(gens) + " Generations", True, (180, 180, 180))
        config.WIN.blit(gen_text, (config.WIN_WIDTH / 2 + 65, train_y + 10))
        draw_menu_options(play_ai_text, ai_y)
        draw_menu_options(reset_text, reset_y)
        pygame.display.update()
        clock.tick(10)
