import pygame
import neat
import random
import os
import pickle
import config as config
from ground import Ground
from cactus import Cactus
from dino import Dino
from game import start, update_cacti, draw


def train_gameplay(genomes, neat_config):
    config.HIGH_SCORE = config.HIGH_SCORE
    ground = Ground()
    cacti = [Cactus(neat_config.WIN_WIDTH + random.randint(0, 250))]

    dinos = []
    nets = []
    ge = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, neat_config)
        nets.append(net)
        dinos.append(Dino())
        g.fitness = 0
        ge.append(g)

    clock = pygame.time.Clock()
    run = True
    score = 0
    ticks = 0

    while run and len(dinos) > 0:
        config.WIN.fill((0, 0, 0))
        clock.tick(120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        if not run:
            start()
        cactus_i = 0
        if cacti[0].passed:
            cactus_i = 1

        for dino in dinos:
            ge[dinos.index(dino)].fitness += 0.1

            output = nets[dinos.index(dino)].activate(
                [dino.y, cacti[cactus_i].x])
            pygame.draw.line(config.WIN, (255, 0, 0), (dino.x + dino.img.get_width() / 2,
                                                       dino.y + dino.img.get_height()),
                             (cacti[cactus_i].x, cacti[cactus_i].y))
            if output[0] > 0.5:
                if not dino.is_jumping:
                    ge[dinos.index(dino)].fitness -= 1
                dino.jump()

            for cactus in cacti:
                if not cactus.passed and dino.x > cactus.x + cactus.img.get_width() + 1:
                    cactus.passed = True
                    ge[dinos.index(dino)].fitness += 5

                if cactus.collide(dino):
                    ge[dinos.index(dino)].fitness -= 0.5
                    nets.pop(dinos.index(dino))
                    ge.pop(dinos.index(dino))
                    dinos.pop(dinos.index(dino))

        ticks += 1
        if ticks % (config.SPEED * 2) == 0:
            score += 1

        if score == 50:
            run = False
        update_cacti(cacti)
        draw(1, ground, dinos, cacti, score, len(dinos))
    config.GEN += 1


def ai_gameplay(genome, neat_config):
    ground = Ground()
    cacti = [Cactus(config.WIN_WIDTH + random.randint(0, 250))]

    ge = genome
    net = neat.nn.FeedForwardNetwork.create(ge, neat_config)
    dino = Dino()

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

        cactus_i = 0
        if cacti[0].passed:
            cactus_i = 1

        output = net.activate([dino.y, cacti[cactus_i].x])
        if output[0] > 0.5:
            dino.jump()

        for cactus in cacti:
            if not cactus.passed and dino.x > cactus.x + cactus.img.get_width() + 1:
                cactus.passed = True

            if cactus.collide(dino):
                run = False
        if run:
            ticks += 1
            if ticks % (config.SPEED * 2) == 0:
                score += 1

            update_cacti(cacti)
            draw(2, ground, [dino], cacti, score, 0)
    if config.HIGH_SCORE < score:
        config.HIGH_SCORE = score


def train_ai(generations):
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config.txt')
    neat_config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                     neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(neat_config)

    # p.add_reporter(neat.StdOutReporter(True))
    # stats = neat.StatisticsReporter()
    # p.add_reporter(stats)

    neat_config.Winner = p.run(train_gameplay, generations)

    with open(os.path.join(local_dir, 'ai.pkl'), "wb") as f:
        pickle.dump(neat_config.Winner, f)
        f.close()

    # print('\nBest genome:\n{!s}'.format(config.WINner))


def play_ai():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config.txt')
    neat_config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                     neat.DefaultStagnation, config_path)

    p = neat.Population(neat_config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    try:
        f = open(os.path.join(local_dir, 'ai.pkl'), "rb")
    except FileNotFoundError:
        print("No File named ai.pkl found, creating a new AI with random weights")
        genome = neat.genome.DefaultGenome(0)
        genome.fitness = 0
        ai_gameplay(genome, neat_config)
    else:
        g = pickle.load(f)
        f.close()
        ai_gameplay(g, neat_config)
