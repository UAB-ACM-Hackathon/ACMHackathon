import sys, pygame

class Cursor():

    def __init__(self):
        self.clicking = 0
        
    def update(self):
        position = pygame.mouse.get_pos()
        self.rect.midtop = position

    def click(self, target):
        if not self.clicking:
            self.clicking = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unclick(self):
        self.clicking = 0
        
class Toad(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = pygame.image.load("toad-icon.png")
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.dizzy = 0
        
    def update(self):
        if self.dizzy:
            self.spin()
        else:
            self.walk()
    
    def walk(self):
        new_position = self.rect.move((self.move, 0))
        if self.rect.left < self.area.left or \
            self.rect.right > self.area.right:
            self.move = -self.move
            new_position = self.rect.move((self.move, 0))
            self.image = pygame.transformation.flip(self.image, 1, 0)
        self.rect = new_position
    
    def spin(self):
        center = self.rect.center
        self.dizzy - self.dizzy + 12
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
    pygame.display.set_caption('A GAME')
    
    background = pygame.image.load("game-background.jpg")
    
    screen.blit(background,(0, 0))
    
    pygame.display.flip()

    clock = pygame.time.Clock()
    toad = Toad()
    cursor = Cursor()
    sprites = pygame.sprite.RenderPlain((toad))
    
    going = True
    while going:
        clock.tick(20)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = True
            elif event.type == MOUSEBUTTONDOWN:
                if cursor.click(toad):
                    toad.clicked()
            elif event.type == MOUSEBUTTONUP:
                cursor.unclick()  
        #sprites.update()
    
        screen.blit(background, (0, 0))
        sprites.draw(screen)
        pygame.display.flip()
       
    pygame.quit()

            
if __name__ == '__main__':
    main()