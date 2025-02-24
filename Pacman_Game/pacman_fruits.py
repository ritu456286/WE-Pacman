import pygame
import random
import webbrowser
import time

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)

# Load Pacman icon
Trollicon = pygame.image.load('pacman.png')
pygame.display.set_icon(Trollicon)

# Add music
pygame.mixer.init()
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1, 0.0)

# Load sound effects
win_sound = pygame.mixer.Sound('win.mp3')
lose_sound = pygame.mixer.Sound('lose.mp3')

# Create 8 HTML files with question numbers
for i in range(1, 9):
    with open(f"question_{i}.html", "w") as file:
        file.write(f"<html><body><h1>Question {i}</h1></body></html>")

# This class represents the bar at the bottom that the player controls
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

# This creates all the walls in room 1
def setupRoomOne(all_sprites_list):
    wall_list = pygame.sprite.RenderPlain()
    walls = [
        [0, 0, 6, 600], [0, 0, 600, 6], [0, 600, 606, 6], [600, 0, 6, 606],
        [300, 0, 6, 66], [60, 60, 186, 6], [360, 60, 186, 6], [60, 120, 66, 6],
        [60, 120, 6, 126], [180, 120, 246, 6], [300, 120, 6, 66], [480, 120, 66, 6],
        [540, 120, 6, 126], [120, 180, 126, 6], [120, 180, 6, 126], [360, 180, 126, 6],
        [480, 180, 6, 126], [180, 240, 6, 126], [180, 360, 246, 6], [420, 240, 6, 126],
        [240, 240, 42, 6], [324, 240, 42, 6], [240, 240, 6, 66], [240, 300, 126, 6],
        [360, 240, 6, 66], [0, 300, 66, 6], [540, 300, 66, 6], [60, 360, 66, 6],
        [60, 360, 6, 186], [480, 360, 66, 6], [540, 360, 6, 186], [120, 420, 366, 6],
        [120, 420, 6, 66], [480, 420, 6, 66], [180, 480, 246, 6], [300, 480, 6, 66],
        [120, 540, 126, 6], [360, 540, 126, 6]
    ]
    for item in walls:
        wall = Wall(item[0], item[1], item[2], item[3], blue)
        wall_list.add(wall)
        all_sprites_list.add(wall)
    return wall_list

def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()
    gate.add(Wall(282, 242, 42, 2, white))
    all_sprites_list.add(gate)
    return gate

# This class represents the dots
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("coding.png").convert()
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# This class represents the fruits
class Fruit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("fruit.png").convert()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# This class represents the player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y
        self.change_x = 0
        self.change_y = 0

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def update(self, walls, gate):
        old_x = self.rect.left
        new_x = old_x + self.change_x
        self.rect.left = new_x
        old_y = self.rect.top
        new_y = old_y + self.change_y
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            self.rect.left = old_x
        else:
            self.rect.top = new_y
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                self.rect.top = old_y
        if gate != False:
            gate_hit = pygame.sprite.spritecollide(self, gate, False)
            if gate_hit:
                self.rect.left = old_x
                self.rect.top = old_y

class Ghost(Player):
    def changespeed(self, list, ghost, turn, steps, l):
        try:
            z = list[turn][2]
            if steps < z:
                self.change_x = list[turn][0]
                self.change_y = list[turn][1]
                steps += 1
            else:
                if turn < l:
                    turn += 1
                elif ghost == "clyde":
                    turn = 2
                else:
                    turn = 0
                self.change_x = list[turn][0]
                self.change_y = list[turn][1]
                steps = 0
            return [turn, steps]
        except IndexError:
            return [0, 0]

Pinky_directions = [
    [0, -30, 4], [15, 0, 9], [0, 15, 11], [-15, 0, 23], [0, 15, 7], [15, 0, 3],
    [0, -15, 3], [15, 0, 19], [0, 15, 3], [15, 0, 3], [0, 15, 3], [15, 0, 3],
    [0, -15, 15], [-15, 0, 7], [0, 15, 3], [-15, 0, 19], [0, -15, 11], [15, 0, 9]
]

Blinky_directions = [
    [0, -15, 4], [15, 0, 9], [0, 15, 11], [15, 0, 3], [0, 15, 7], [-15, 0, 11],
    [0, 15, 3], [15, 0, 15], [0, -15, 15], [15, 0, 3], [0, -15, 11], [-15, 0, 3],
    [0, -15, 11], [-15, 0, 3], [0, -15, 3], [-15, 0, 7], [0, -15, 3], [15, 0, 15],
    [0, 15, 15], [-15, 0, 3], [0, 15, 3], [-15, 0, 3], [0, -15, 7], [-15, 0, 3],
    [0, 15, 7], [-15, 0, 11], [0, -15, 7], [15, 0, 5]
]

Inky_directions = [
    [30, 0, 2], [0, -15, 4], [15, 0, 10], [0, 15, 7], [15, 0, 3], [0, -15, 3],
    [15, 0, 3], [0, -15, 15], [-15, 0, 15], [0, 15, 3], [15, 0, 15], [0, 15, 11],
    [-15, 0, 3], [0, -15, 7], [-15, 0, 11], [0, 15, 3], [-15, 0, 11], [0, 15, 7],
    [-15, 0, 3], [0, -15, 3], [-15, 0, 3], [0, -15, 15], [15, 0, 15], [0, 15, 3],
    [-15, 0, 15], [0, 15, 11], [15, 0, 3], [0, -15, 11], [15, 0, 11], [0, 15, 3],
    [15, 0, 1]
]

Clyde_directions = [
    [-30, 0, 2], [0, -15, 4], [15, 0, 5], [0, 15, 7], [-15, 0, 11], [0, -15, 7],
    [-15, 0, 3], [0, 15, 7], [-15, 0, 7], [0, 15, 15], [15, 0, 15], [0, -15, 3],
    [-15, 0, 11], [0, -15, 7], [15, 0, 3], [0, -15, 11], [15, 0, 9]
]

pl = len(Pinky_directions) - 1
bl = len(Blinky_directions) - 1
il = len(Inky_directions) - 1
cl = len(Clyde_directions) - 1

pygame.init()
screen = pygame.display.set_mode([606, 606])
pygame.display.set_caption('Pacman with Fruits')
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

w = 303 - 16
p_h = (7 * 60) + 19
m_h = (4 * 60) + 19
b_h = (3 * 60) + 19
i_w = 303 - 16 - 32
c_w = 303 + (32 - 16)

def startGame():
    all_sprites_list = pygame.sprite.RenderPlain()
    block_list = pygame.sprite.RenderPlain()
    fruit_list = pygame.sprite.RenderPlain()
    monsta_list = pygame.sprite.RenderPlain()
    pacman_collide = pygame.sprite.RenderPlain()

    wall_list = setupRoomOne(all_sprites_list)
    gate = setupGate(all_sprites_list)

    p_turn = 0
    p_steps = 0
    b_turn = 0
    b_steps = 0
    i_turn = 0
    i_steps = 0
    c_turn = 0
    c_steps = 0

    Pacman = Player(w, p_h, "pacman.png")
    all_sprites_list.add(Pacman)
    pacman_collide.add(Pacman)

    Blinky = Ghost(w, b_h, "error.png")
    monsta_list.add(Blinky)
    all_sprites_list.add(Blinky)

    Pinky = Ghost(w, m_h, "deadline.png")
    monsta_list.add(Pinky)
    all_sprites_list.add(Pinky)

    Inky = Ghost(i_w, m_h, "demotivated.png")
    monsta_list.add(Inky)
    all_sprites_list.add(Inky)

    Clyde = Ghost(c_w, m_h, "infinite-time.png")
    monsta_list.add(Clyde)
    all_sprites_list.add(Clyde)

    # Place dots and fruits
    positions = []
    for row in range(19):
        for column in range(19):
            if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                continue
            else:
                positions.append((30 * column + 6 + 26, 30 * row + 6 + 26))

    # Randomly select 8 positions for fruits
    fruit_positions = random.sample(positions, 8)
    for pos in positions:
        if pos in fruit_positions:
            fruit = Fruit(pos[0], pos[1])
            fruit_list.add(fruit)
            all_sprites_list.add(fruit)
        else:
            block = Block(pos[0], pos[1])
            block_list.add(block)
            all_sprites_list.add(block)

    bll = len(block_list) + len(fruit_list)
    score = 0
    done = False
    paused = False

    while done == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(-30, 0)
                if event.key == pygame.K_RIGHT:
                    Pacman.changespeed(30, 0)
                if event.key == pygame.K_UP:
                    Pacman.changespeed(0, -30)
                if event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, 30)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(30, 0)
                if event.key == pygame.K_RIGHT:
                    Pacman.changespeed(-30, 0)
                if event.key == pygame.K_UP:
                    Pacman.changespeed(0, 30)
                if event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, -30)

        if not paused:
            Pacman.update(wall_list, gate)

            returned = Pinky.changespeed(Pinky_directions, False, p_turn, p_steps, pl)
            p_turn = returned[0]
            p_steps = returned[1]
            Pinky.changespeed(Pinky_directions, False, p_turn, p_steps, pl)
            Pinky.update(wall_list, False)

            returned = Blinky.changespeed(Blinky_directions, False, b_turn, b_steps, bl)
            b_turn = returned[0]
            b_steps = returned[1]
            Blinky.changespeed(Blinky_directions, False, b_turn, b_steps, bl)
            Blinky.update(wall_list, False)

            returned = Inky.changespeed(Inky_directions, False, i_turn, i_steps, il)
            i_turn = returned[0]
            i_steps = returned[1]
            Inky.changespeed(Inky_directions, False, i_turn, i_steps, il)
            Inky.update(wall_list, False)

            returned = Clyde.changespeed(Clyde_directions, "clyde", c_turn, c_steps, cl)
            c_turn = returned[0]
            c_steps = returned[1]
            Clyde.changespeed(Clyde_directions, "clyde", c_turn, c_steps, cl)
            Clyde.update(wall_list, False)

            blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)
            if len(blocks_hit_list) > 0:
                score += len(blocks_hit_list)

            fruits_hit_list = pygame.sprite.spritecollide(Pacman, fruit_list, True)
            if len(fruits_hit_list) > 0:
                score += len(fruits_hit_list)
                paused = True
                random_html = random.randint(1, 8)
                webbrowser.open(f"question_{random_html}.html")
                time.sleep(5)  # Wait for 5 seconds before resuming the game
                paused = False

        screen.fill(black)
        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        monsta_list.draw(screen)

        text = font.render("Score: " + str(score) + "/" + str(bll), True, red)
        screen.blit(text, [10, 10])

        if score == bll:
            pygame.mixer.music.stop()
            win_sound.play()
            doNext("Game Won!", 145, all_sprites_list, block_list, fruit_list, monsta_list, pacman_collide, wall_list, gate)

        monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)
        if monsta_hit_list:
            pygame.mixer.music.stop()
            lose_sound.play()
            doNext("Game Over", 235, all_sprites_list, block_list, fruit_list, monsta_list, pacman_collide, wall_list, gate)

        pygame.display.flip()
        clock.tick(10)

def doNext(message, left, all_sprites_list, block_list, fruit_list, monsta_list, pacman_collide, wall_list, gate):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    del all_sprites_list
                    del block_list
                    del fruit_list
                    del monsta_list
                    del pacman_collide
                    del wall_list
                    del gate
                    startGame()

        w = pygame.Surface((400, 200))
        w.set_alpha(10)
        w.fill((128, 128, 128))
        screen.blit(w, (100, 200))

        text1 = font.render(message, True, white)
        screen.blit(text1, [left, 233])

        text2 = font.render("To play again, press ENTER.", True, white)
        screen.blit(text2, [135, 303])
        text3 = font.render("To quit, press ESCAPE.", True, white)
        screen.blit(text3, [165, 333])

        pygame.display.flip()
        clock.tick(10)

startGame()
pygame.quit()