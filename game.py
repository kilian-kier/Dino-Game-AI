import pygame
import random
import os
import neat
import pickle

pygame.font.init()

WIN_WIDTH = 800
WIN_HEIGHT = 500
STAT_FONT = pygame.font.SysFont("comicsans", 32)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Dino Game AI")
SPEED = 12
GEN = 0
HIGHSCORE = 0


def load_image(name):
    fullname = os.path.join(os.path.join(
        os.path.dirname(__file__), 'imgs'), name)
    image = pygame.image.load(fullname).convert_alpha()
    return image


def load_sprite_sheet(sheetname, nx, scale):
    fullname = os.path.join(os.path.join(
        os.path.dirname(__file__), 'imgs'), sheetname)
    sheet = pygame.image.load(fullname)
    sheet = pygame.transform.scale(
        sheet, (int(sheet.get_width() * scale), int(sheet.get_height() * scale)))
    sheet = sheet.convert_alpha()

    sheet_rect = sheet.get_rect()

    imgs = []

    sizex = sheet_rect.width/nx
    sizey = sheet_rect.height

    for i in range(0, nx):
        rect = pygame.Rect((i*sizex, 0, sizex, sizey))
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image = image.convert_alpha()
        image.blit(sheet, (0, 0), rect)

        imgs.append(image)

    return imgs


dino_imgs = load_sprite_sheet('dino.png', 4, 0.6)
cacti_imgs = load_sprite_sheet('cacti.png', 4, 1)
grd_img = pygame.transform.scale2x(load_image("ground.png"))
GROUND = WIN_HEIGHT - grd_img.get_height()


class Dino:
    IMGS = dino_imgs
    ANIMATION_TIME = 5
    JUMP_N = 10.5

    def __init__(self):
        self.x = 40
        self.y = GROUND - self.IMGS[0].get_height() + 25
        self.vel = 0
        self.mass = 1
        self.is_jumping = False
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        if not self.is_jumping:
            self.vel = self.JUMP_N
            self.is_jumping = True

    def move(self):
        if self.is_jumping == True:
            if self.vel >= -self.JUMP_N:
                self.y -= (self.vel * abs(self.vel)) * 0.5
                self.vel -= 1.5
            else:
                self.vel = 0
                self.is_jumping = False

    def draw(self):
        if self.is_jumping:
            self.img = self.IMGS[0]
            self.img_count = 0
        else:
            self.img_count += 1
            if self.img_count <= self.ANIMATION_TIME:
                self.img = self.IMGS[1]
            elif self.img_count <= self.ANIMATION_TIME*2:
                self.img = self.IMGS[2]
            elif self.img_count <= self.ANIMATION_TIME*3:
                self.img = self.IMGS[1]
                self.img_count = 0
        WIN.blit(self.img, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Cactus:
    IMGS = cacti_imgs
    VEL = SPEED

    def __init__(self, x):
        self.x = x
        self.y = GROUND - self.IMGS[0].get_height() + 25
        self.img = self.IMGS[random.randint(0, 3)]
        self.passed = False

    def move(self):
        self.x -= self.VEL

    def draw(self):
        WIN.blit(self.img, (self.x, self.y))

    def collide(self, dino):
        '''dino_mask = dino.get_mask()
        cactus_mask = pygame.mask.from_surface(self.img)
        offset_x = self.x - dino.x
        offset_y = self.y - int(dino.y)

        point = cactus_mask.overlap(dino_mask, (offset_x, offset_y))
        print((dino.x + dino.img.get_width(), dino.y), (self.x, self.y), point)
        if point:
            return True
        else:
            return False'''
        dino_rect = pygame.rect.Rect(
            (dino.x, dino.y, dino.img.get_width(), dino.img.get_height()))
        cactus_rect = pygame.rect.Rect(
            (self.x, self.y, self.img.get_width(), self.img.get_height()))
        if cactus_rect.colliderect(dino_rect):
            return True
        else:
            return False


class Ground:
    IMG = grd_img
    VEL = SPEED
    WIDTH = IMG.get_width()

    def __init__(self):
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        elif self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self):
        WIN.blit(self.IMG, (self.x1, GROUND))
        WIN.blit(self.IMG, (self.x2, GROUND))


def draw(mode, ground, dinos, cacti, score, alive):
    ground.move()
    ground.draw()
    for cact in cacti:
        cact.move()
        cact.draw()
    for dino in dinos:
        dino.move()
        dino.draw()
    score_text = STAT_FONT.render("Score: " + str(score), 1, (180, 180, 180))
    WIN.blit(score_text, (WIN_WIDTH - score_text.get_width() - 15, 10))
    if mode != 1:
        high_score_text = STAT_FONT.render(
            "Highcore: " + str(HIGHSCORE), 1, (180, 180, 180))
        WIN.blit(high_score_text, (WIN_WIDTH - score_text.get_width() -
                 high_score_text.get_width() - 30, 10))
    if mode == 1:
        gen_text = STAT_FONT.render("Gen: " + str(GEN), 1, (180, 180, 180))
        WIN.blit(gen_text, (15, 10))
        alive_text = STAT_FONT.render(
            "Alive: " + str(alive), 1, (180, 180, 180))
        WIN.blit(alive_text, (15, gen_text.get_height() + 20))
    pygame.display.flip()
    pygame.display.update()


def update_cacti(cacti):
    rem = []
    for cact in cacti:
        if cact.x + cact.img.get_width() < 0:
            rem.append(cact)
    for r in rem:
        cacti.remove(r)

    if cacti[-1].x < WIN_WIDTH - cacti_imgs[0].get_width():
        cacti.append(Cactus(cacti[-1].x + random.randint(200, 800)))


def real_player():
    global HIGHSCORE
    dino = Dino()
    ground = Ground()
    cacti = [Cactus(WIN_WIDTH + random.randint(0, 250))]

    clock = pygame.time.Clock()
    run = True

    score = 0
    ticks = 0

    while run:
        WIN.fill((0, 0, 0))
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
            if ticks % (SPEED * 2) == 0:
                score += 1
    if HIGHSCORE < score:
        HIGHSCORE = score


def train_ai(genomes, config):
    global GEN
    global HIGHSCORE
    HIGHSCORE = HIGHSCORE
    ground = Ground()
    cacti = [Cactus(WIN_WIDTH + random.randint(0, 250))]

    dinos = []
    nets = []
    ge = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        dinos.append(Dino())
        g.fitness = 0
        ge.append(g)

    clock = pygame.time.Clock()
    run = True
    score = 0
    ticks = 0

    while run and len(dinos) > 0:
        WIN.fill((0, 0, 0))
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
            pygame.draw.line(WIN, (255, 0, 0), (dino.x+dino.img.get_width()/2,
                             dino.y + dino.img.get_height()), (cacti[cactus_i].x, cacti[cactus_i].y))
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
        if ticks % (SPEED * 2) == 0:
            score += 1

        if score == 50:
            run = False
        update_cacti(cacti)
        draw(1, ground, dinos, cacti, score, len(dinos))
    GEN += 1


def play_ai(genome, config):
    global HIGHSCORE
    ground = Ground()
    cacti = [Cactus(WIN_WIDTH + random.randint(0, 250))]

    ge = genome
    net = neat.nn.FeedForwardNetwork.create(ge, config)
    dino = Dino()

    clock = pygame.time.Clock()
    run = True
    score = 0
    ticks = 0

    while run:
        WIN.fill((0, 0, 0))
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
            if ticks % (SPEED * 2) == 0:
                score += 1

            update_cacti(cacti)
            draw(2, ground, [dino], cacti, score, 0)
    if HIGHSCORE < score:
        HIGHSCORE = score


def train(generations):
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config.txt')
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    # p.add_reporter(neat.StdOutReporter(True))
    # stats = neat.StatisticsReporter()
    # p.add_reporter(stats)

    winner = p.run(train_ai, generations)

    with open(os.path.join(local_dir, 'ai.pkl'), "wb") as f:
        pickle.dump(winner, f)
        f.close

    # print('\nBest genome:\n{!s}'.format(winner))


def ai():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config.txt')
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    try:
        f = open(os.path.join(local_dir, 'ai.pkl'), "rb")
    except FileNotFoundError:
        genome = neat.genome.DefaultGenome(0)
        genome.fitness = 0
        play_ai(genome, config)
    else:
        g = pickle.load(f)
        f.close
        play_ai(g, config)


def start():
    global HIGHSCORE
    real_heigth = WIN_HEIGHT / 5 * 1
    real = STAT_FONT.render("Play", 1, (180, 180, 180))

    train_heigth = WIN_HEIGHT / 5 * 2
    train_text = STAT_FONT.render("Train AI", 1, (180, 180, 180))

    ai_heigth = WIN_HEIGHT / 5 * 3
    play_ai = STAT_FONT.render("Play AI", 1, (180, 180, 180))

    reset_heigth = WIN_HEIGHT / 5 * 4
    reset = STAT_FONT.render("Reset", 1, (180, 180, 180))

    clock = pygame.time.Clock()

    gen_input = "10"

    while True:
        mouse = pygame.mouse.get_pos()
        if gen_input == "":
            gen_input = "0"
        try:
            gens = int(gen_input)
        except ValueError:
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse[0] >= WIN_WIDTH/2 - 50 and mouse[0] <= WIN_WIDTH/2 + 50:
                    if mouse[1] >= real_heigth and mouse[1] <= real_heigth + 40:
                        real_player()
                    elif mouse[1] >= train_heigth and mouse[1] <= train_heigth + 40:
                        train(gens)
                    elif mouse[1] >= ai_heigth and mouse[1] <= ai_heigth + 40:
                        ai()
                    elif mouse[1] >= reset_heigth and mouse[1] <= reset_heigth + 40:
                        HIGHSCORE = 0
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
                elif event.unicode >= "0" and event.unicode <= "9":
                    gen_input += event.unicode

        WIN.fill((0, 0, 0))
        WIN.blit(real, (WIN_WIDTH/2 - real.get_width()/2, real_heigth + 10))
        pygame.draw.rect(WIN, (180, 180, 180), (WIN_WIDTH /
                         2 - 50, real_heigth, 100, 40), 2, 5)
        WIN.blit(train_text, (WIN_WIDTH/2 -
                 train_text.get_width()/2, train_heigth + 10))
        pygame.draw.rect(WIN, (180, 180, 180), (WIN_WIDTH /
                         2 - 50, train_heigth, 100, 40), 2, 5)
        gen_text = STAT_FONT.render(
            str(gens) + " Generations", 1, (180, 180, 180))
        WIN.blit(gen_text, (WIN_WIDTH/2 +
                 65, train_heigth + 10))
        WIN.blit(play_ai, (WIN_WIDTH/2 - play_ai.get_width()/2, ai_heigth + 10))
        pygame.draw.rect(WIN, (180, 180, 180), (WIN_WIDTH /
                         2 - 50, ai_heigth, 100, 40), 2, 5)
        WIN.blit(reset, (WIN_WIDTH/2 - reset.get_width()/2, reset_heigth + 10))
        pygame.draw.rect(WIN, (180, 180, 180), (WIN_WIDTH /
                         2 - 50, reset_heigth, 100, 40), 2, 5)
        pygame.display.update()
        clock.tick(10)


if __name__ == "__main__":
    start()
