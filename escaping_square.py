import pygame
from random import randint
from math import sin, cos
import shelve

pygame.init()
WIN_SIZE = (600, 600)

win = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption('SquarEscape')

class Player():
    def __init__(self):
        self.x = WIN_SIZE[0]//2
        self.y = WIN_SIZE[0]//2
        self.vel = 1
        size = randint(20,100)
        self.width = size
        self.hight = size


    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 0), (self.x, self.y, self.width, self.hight))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vel
        if keys[pygame.K_RIGHT] and self.x + self.vel + self.width <= WIN_SIZE[0]:
            self.x += self.vel
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.vel
        if keys[pygame.K_DOWN] and self.y + self.vel + self.hight <= WIN_SIZE[1]:
            self.y += self.vel

    def got_hit(self, score, best_score):
        if best_score < score:
            with shelve.open('hiscore.txt') as f:
                f['hiscore'] = score
        font2 = pygame.font.SysFont('comicsans', 100)
        text2 = font2.render(f'Your score: {score}', 0, (255,255,255))
        win.blit(text2, (WIN_SIZE[0]//2 - (text2.get_width()//2), WIN_SIZE[1]//2))
        pygame.display.update()
        for i in range(50):
            pygame.time.delay(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        main()


class Enemy():
    def __init__(self,x ,y, width = 20, hight = 20):
        self.x = x
        self.y = y
        self.vel = 1
        self.width = width
        self.hight = hight
        self.direction = randint(1, 359)

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.hight))

    def y_dir(self):
        return sin(self.direction)

    def x_dir(self):
        return cos(self.direction)

    def move(self):
        if 0 < self.direction < 180:
            self.x += self.vel * self.x_dir()
        if 180 < self.direction < 360:
            self.x -= self.vel * self.x_dir()
        if 0 < self.direction < 90 or 270 < self.direction < 360:
            self.y += self.vel * self.y_dir()
        if 90 < self.direction < 270:
            self.y += self.vel * self.y_dir()

        self.change_dir()

    def change_dir(self):

        if self.x <= 0:
            self.direction = randint(1, 179)
            self.x += 5

        if self.x + self.width >= WIN_SIZE[0]:
            self.direction = randint(179, 359)
            self.x -= 10
        if self.y <= 0:
            self.direction = randint(179, 269)
            self.y += 10
        if self.y + self.hight >= WIN_SIZE[1]:
            if randint(1, 2) == 1:
                self.direction = randint(1, 89)
                self.y -= 10
            else:
                self.direction = randint(271, 359)
                self.y -= 10




def main():
    def render_win():
        win.fill((0, 0, 0))
        player.draw(win)
        for enemy in enemys:
            enemy.draw(win)
        score_text = font.render(f'HiScore:  {best_score}', True, (255, 255, 255))
        win.blit(score_text, (WIN_SIZE[0]-150, 10))
        pygame.display.update()

    run = True
    clock = pygame.time.Clock()
    player = Player()
    enemys = [Enemy(WIN_SIZE[0] - WIN_SIZE[0] // 10, WIN_SIZE[1] - WIN_SIZE[0] // 10, randint(10, 80), randint(10, 80)),
              Enemy(WIN_SIZE[0] - WIN_SIZE[0] // 10, WIN_SIZE[1] // 10, randint(10, 80), randint(10, 80)),
              Enemy(WIN_SIZE[0] // 10, WIN_SIZE[1] - WIN_SIZE[0] // 10, randint(10, 80), randint(10, 80)),
              Enemy(WIN_SIZE[0] // 10, WIN_SIZE[1] // 10, randint(10, 80), randint(10, 80))]
    game_start = 0
    with shelve.open('hiscore.txt') as f:
        try:
            best_score = f['hiscore']
        except KeyError:
            f['hiscore'] = 0
            best_score = f['hiscore']
            print ('err')

    font = pygame.font.SysFont('comic sans', 24)

    while run:
        clock.tick(60)
        game_start += 1
        if game_start % 180 == 0 :
            player.vel += 0.5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        player.move(keys)
        for enemy in enemys:
            if game_start % 180 == 0:
                enemy.vel += 0.5
            enemy.move()
            if ((enemy.x < player.x < enemy.x + enemy.width) or (enemy.x < player.x + player.width < enemy.x + enemy.width) or
                    (player.x < enemy.x < player.x +player.width) or (player.x < enemy.x + enemy.width < player.x + player.width)):
                if ((enemy.y < player.y < enemy.y + enemy.hight) or (enemy.y < player.y + player.hight < enemy.y + enemy.hight) or
                     (player.y < enemy.y < player.y +player.hight) or (player.y < enemy.y + enemy.hight < player.y + player.hight)):
                        player.got_hit(game_start//60, best_score)

        render_win()

    pygame.quit()

if __name__ == '__main__':
    main()