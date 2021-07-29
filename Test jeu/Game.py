import time

import pygame
import pytmx
import pyscroll
from player import Player


class Game:

    def __init__(self):

        #Créer la fenêtre du jeu
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Pygamon - Adventure")

        #Charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())
        map_layer.zoom = 1.5  # Pour le zoom
        self.map ='world'

        #Générer un joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        #Définir une liste qui stocke les rectangles de collisions
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type =="collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        #Dessiner la carte
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        #définir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.change_animation('up1')
            self.player.move_up()
            self.player.change_animation('up2')
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.change_animation('down1')
            self.player.move_down()
            self.player.change_animation('down2')
            self.player.move_down()
        elif pressed[pygame.K_LEFT]:
            self.player.change_animation('left1')
            self.player.move_left()
            self.player.change_animation('left2')
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.player.change_animation('right1')
            self.player.move_right()
            self.player.change_animation('right2')
            self.player.move_right()

    def switch_house(self):
        # Charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('house.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.5  # Pour le zoom

        # Définir une liste qui stocke les rectangles de collisions
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner la carte
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # définir le rectangle de collision pour sortir dans la maison
        enter_house = tmx_data.get_object_by_name('exit_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        #recuperer le point d'apparition dans la maison
        spawn_house_point = tmx_data.get_object_by_name('spawn_house')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 20

    def switch_world(self):
        # Charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.5  # Pour le zoom

        # Définir une liste qui stocke les rectangles de collisions
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner la carte
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # définir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # recuperer le point d'apparition dans le monde
        spawn_house_point = tmx_data.get_object_by_name('enter_house_exit')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y + 20

    def update(self):
        self.group.update()

        #Vérification entrée maison
        if self.map =='world' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = 'house'

        # Vérification sortie maison
        if self.map =='house' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_world()
            self.map = 'world'

        #Vérification collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):

        clock = pygame.time.Clock()

        #Boucle du jeu
        running = True
        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect) #Centrer la caméra sur le joueur
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60) #Les fps

        pygame.quit()