import os, pygame
from pygame.locals import *
from pygame.compat import geterror

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

def load_image(name):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    return image, image.get_rect()

def load_sound(name):
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound
    
class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('cursor.png')
        self.clicking = 0
        
    def update(self):
        position = pygame.mouse.get_pos()
        self.rect.midtop = position
        if self.clicking:
            self.rect.move_ip(10, 10)

    def click(self, target):
        if not self.clicking:
            self.clicking = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unclick(self):
        self.clicking = 0
        
class Toad(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('blue-toad.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 0, 250
        self.move = 9
        self.dizzy = 0

    def update(self):
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        newPosition = self.rect.move((self.move, 0))
        if self.rect.left < self.area.left or \
            self.rect.right > self.area.right:
            self.move = -self.move
            newPosition = self.rect.move((self.move, 0))
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = newPosition

    def _spin(self):
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def clicked(self):
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image

def main():

    pygame.init()
    size = width, height = 800, 500

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Shroom Clicker')
    pygame.mouse.set_visible(0)
    
    background = pygame.image.load("game-background.jpg")
    
    screen.blit(background,(0, 0))
    
    pygame.display.flip()

    clock = pygame.time.Clock()
    miss_sound = load_sound('Toad3.wav')
    click_sound = load_sound('Toad7.wav')
    toad = Toad()
    cursor = Cursor()
    sprites = pygame.sprite.RenderPlain((cursor, toad))
    going = True
    while going:
        clock.tick(200)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                if cursor.click(toad):
                    click_sound.play() 
                    toad.clicked()
                else:
                    miss_sound.play()
            elif event.type == MOUSEBUTTONUP:
                cursor.unclick()  
        sprites.update()
    
        screen.blit(background, (0, 0))
        sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()
            
if __name__ == '__main__':
    main()