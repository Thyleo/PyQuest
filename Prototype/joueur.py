import pygame
import time

class Joueur(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('player.png')
        self.image = self.get_image(0,64)
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect()  #Corps du personnage
        self.position = [x, y]  # Les coordonnées du personnage
        self.speed = 3
        self.images={
            'left' : self.get_image(0, 32),
            'right' : self.get_image(0, 64)
        } #Dictionnaire des images du joueur
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()

    def save_location(self): self.old_position = self.position.copy()

    def move_right(self): self.position[0] += self.speed

    def move_left(self): self.position[0] -= self.speed

    def move_down(self): self.position[1] += 5

    def move_up(self):
         self.position[1] -= 5

    def change_animation(self, name):
        self.image = self.images[name]
        self.image.set_colorkey([0, 0, 0])

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom