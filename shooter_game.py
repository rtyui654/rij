#Создай собственный Шутер!
from random import randint

from pygame import *
from time import time as timer
mixer.init()

font.init()
font1 = font.SysFont('Arial',35)
font2 = font.SysFont('Arial',80)
win = font2.render("YOU WIN", True,(0,255,0))
lose = font2.render("YOU LOSE", True,(255,0,0))
loes = 0
score = 0



class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,seze_x,seze_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(seze_x, seze_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        Window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys [K_LEFT] and self.rect.x >5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x <630:
            self.rect.x += self.speed
        if keys [K_UP] and self.rect.y >5:
            self.rect.y -= self.speed
        if keys [K_DOWN] and self.rect.y <430:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx,self.rect.top, 15, 20, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global loes 
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            loes += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -=self.speed
        if self.rect.y < 0:
            self.kill()


    


win_width = 700
win_height = 500
Window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("galaxy.jpg"),(win_width, win_height))

ship = Player('rocket.png', 5, win_height-100, 80, 100 ,7)
bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png',randint(80, 620), -40, 80,50, randint(1,5))
    monsters.add(monster)
for i in range(5):
    asteroid = Enemy('asteroid.png',randint(80, 620), -40, 80,50, randint(1,5))
    asteroids.add(asteroid)
life = 3
finish = False
run = True
fire_sound = mixer.Sound('fire.ogg')

rel_time = False
run = True
fire_sound = mixer.Sound("fire.ogg")
num_fire = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <5 and rel_time != True:
                    fire_sound.play()
                    ship.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time != True:
                    rel_time = True
                    last_time = timer()

    if not finish:
        Window.blit(background,(0,0))

        text = font1.render(f'Счёт:{score}', True,(255,255,255))
        Window.blit(text,(10,20))

        text_loes = font1.render(f'Пропущено:{loes}', True,(255,255,255))
        Window.blit(text_loes,(10,50))

        ship.reset()
        ship.update()
        monsters.draw(Window)
        monsters.update()
        bullets.draw(Window)
        bullets.update()
        asteroids.draw(Window)
        asteroids.update()
        life_text = font1.render(str(life), True, (0,255,0))
        Window.blit(life_text,(650,10))

        collides = sprite.groupcollide(bullets, monsters, True, True)
        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font1.render('ПЕРЕЗАРЯДКА', True, (100,200,100))
                Window.blit(reload,(250,450))
            else:
                num_fire = 0
                rel_time = False
        for i in collides:
            score += 1
            monster = Enemy('ufo.png',randint(80, 620), -40, 80,50, randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters,False):
            finish = True
            Window.blit(lose,(200,200))
        if sprite.spritecollide(ship, asteroids,False):
            life -= 1
            asteroid = Enemy('asteroid.png',randint(80, 620), -40, 80,50, randint(1,5))
            asteroids.add(asteroid)
            finish = True
            Window.blit(lose,(200,200))
        if score > 9:
            finish = True
            Window.blit(win,(200,200))
        if life < 1:
            finish = True
            Window.blit(lose,(200,200))
        
    else:
        finish = False
        score = 0
        loes = 0
        life = 3
        rel_time = False
        num_fire = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(5):
            monster = Enemy('ufo.png',randint(80, 620), -40, 80,50, randint(1,5))
            monsters.add(monster)
        for i in range(5):
            asteroid = Enemy('asteroid.png',randint(80, 620), -40, 80,50, randint(1,5))
            asteroids.add(asteroid)


    display.update()
    time.delay(20)

        
