from pygame import *
from random import randint
from time import time as timer

font.init()
mixer.init()
mix = mixer.Sound('fire.ogg')
mixer.music.load('space.ogg')
mixer.music.play()

win = display.set_mode(
    (700,500)
)

bg = transform.scale(
    image.load('galaxy.jpg'),(700,500)
)


live = 10
class GameSprite(sprite.Sprite):
    def __init__(self, play_image, p_x, p_y, p_speed):
        super().__init__()
        self.image = transform.scale(image.load(play_image), (70, 60))
        self.speed = p_speed
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


pat = -10
class Player(GameSprite):
    
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 635:
            self.rect.x += self.speed

    def fire(self):
        global pat
        bl = Bullet('bullet.png', self.rect.centerx, self.rect.top, 4)
        puls.add(bl)
        pat += 1


class Enemy(GameSprite):
    def update(self):
        if self.rect.y < 429:
            self.rect.y += self.speed

        else:
            global live
            self.rect.x = randint(0,630)
            self.rect.y = randint(0,50)
            live -= 1


w = 0
class Bullet(GameSprite):
    def __init__(self, play_image, p_x, p_y, p_speed):
        super().__init__(play_image, p_x, p_y, p_speed)
        self.image = transform.scale(image.load(play_image), (20, 10))
        
    def update(self):
        if self.rect.y > 0:
            self.rect.y -=  self.speed
        else:
            self.kill()
          
         
def res():
    mas.draw(win)
    mas.update()
    test.update()
    pl1.reset()
    pl1.update()
    puls.draw(win)
    puls.update()
    aster.draw(win)
    aster.update() 
    

test = Bullet('bullet.png',0,0,4)

lt1 = Enemy('ufo.png',0,0,3)
lt2 = Enemy('ufo.png',randint(0,140),randint(0,50),randint(1,3))
lt3 = Enemy('ufo.png',randint(140,280),randint(0,50),randint(1,3))
lt4 = Enemy('ufo.png',randint(280,420),randint(0,50),randint(1,3))
lt5 = Enemy('ufo.png',randint(420,560),randint(0,50),randint(1,3))

pl1 = Player('rocket.png',350,400,10)


mas = sprite.Group()
mas.add(lt1)
mas.add(lt2)
mas.add(lt3)
mas.add(lt4)
mas.add(lt5)


aster = sprite.Group()
for i in range(5):
    ast = Enemy('asteroid.png',randint(0,560),randint(0,30),randint(1,2))
    aster.add(ast)



puls = sprite.Group()


clock = time.Clock()

fon = font.SysFont(None,20)
fon1 = font.SysFont(None,150)



finish = False
game = True
nfir = 0
reltim = False
lasst = None
while game:
    
    win.blit(bg,(0,0))

    if finish == False:
        sp_list = sprite.groupcollide(mas, puls,True,True)
        for i in sp_list :
            lt = Enemy('ufo.png',randint(0,560),randint(0,50),randint(1,3))
            mas.add(lt)
            w += 1
        
        res()
        
        if sprite.spritecollide(pl1, mas, True):
            lt = Enemy('ufo.png',randint(0,560),randint(0,50),randint(1,3))
            mas.add(lt)
            live -= 1
            if live == 0:
                finish = True


        if sprite.spritecollide(pl1, aster, False):
            live -= 1
            if live == 0:
                finish = True



        if live == 0:
            finish = True
                
        if w > 10:
            finish = True
        
        


    wi = fon.render(
            'Счет:'+str(w),True,(255,255,255)
    )
    win.blit(wi,(10,25))       
    li = fon.render(
            'Жизни:'+str(live),True,(255,255,255)
        )
    win.blit(li,(10,10)) 
    wiiiii = fon1.render(
            'win!',True,(255,255,255)
        )
    looooo = fon1.render(
            'loos!',True,(255,255,255)
        )
    if w > 10:
        win.blit(wiiiii, (250,200))
    if live == 0:
        win.blit(looooo, (250,200))

    if reltim == True:
        now = timer()
        
        if now - last < 4:
            rel = fon.render('перезарядка',True,(255,255,255))
            win.blit(rel, (260,460))
        else:
            reltim = False


    display.update()
    clock.tick(60)
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if pat != 0:
                    nfir += 1
                    pl1.fire()
                    mix.play() 
                    
                        

                if nfir >= 10 and reltim == False:
                    last = timer()
                    reltim = True  
                    
            if e.key == K_r and finish != True and  pat == 0:
                finish = False
                pat = -10
                for i in range(3):
                    ast = Enemy('asteroid.png',randint(0,560),randint(0,30),randint(1,2))
                    aster.add(ast)
            
            
                
