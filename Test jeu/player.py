import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('player.png')
        self.image = self.get_image(32,0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.images={
            'down1': self.get_image(0,0),
            'left1': self.get_image(0, 32),
            'right1': self.get_image(0, 64),
            'up1': self.get_image(0, 96),
            'calm_down': self.get_image(32,0),
            'calm_left': self.get_image(32, 32),
            'calm_right': self.get_image(32, 64),
            'calm_up': self.get_image(32, 96),
            'down2': self.get_image(96, 0),
            'left2': self.get_image(96, 32),
            'right2': self.get_image(96, 64),
            'up2': self.get_image(96, 96)
        }
        self.speed = 3
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()

    def save_location(self):
        self.old_position = self.position.copy()

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def change_animation(self, name):
        self.image = self.images[name]
        self.image.set_colorkey([0, 0, 0])

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_up(self): self.position[1] -= self.speed

    def move_down(self): self.position[1] += self.speed

    def move_left(self): self.position[0] -= self.speed

    def move_right(self): self.position[0] += self.speed

    def get_image(self, x, y):
        image = pygame.Surface([32,32])
        image.blit(self.sprite_sheet, (0,0), (x, y, 32, 32))
        return image