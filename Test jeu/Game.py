import pygame
import pytmx
import pyscroll
import time
from player import Player


class Game:

    def __init__(self):
        #Création de la fenêtre du jeu
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("PyAdventure - The game")

        #Chargement de la carte
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map='world'

        #Génerer un joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        #Les collisions
        self.walls = []
        for object in tmx_data.objects:
            if object.type =="collision":
                self.walls.append(pygame.Rect(object.x, object.y, object.width, object.height))

        #Chargement du groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        #Entrée batiment
        entrée = tmx_data.get_object_by_name('entrée')
        self.enter_house_rect = pygame.Rect(entrée.x, entrée.y, entrée.width, entrée.height)


    def switch_house(self):
        # Chargement de la carte
        tmx_data = pytmx.util_pygame.load_pygame('house.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        # Les collisions
        self.walls = []
        for object in tmx_data.objects:
            if object.type == "collision":
                self.walls.append(pygame.Rect(object.x, object.y, object.width, object.height))

        # Chargement du groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # sortie batiment
        sortie = tmx_data.get_object_by_name('sortie')
        self.sortie_house_rect = pygame.Rect(sortie.x, sortie.y, sortie.width, sortie.height)

        # Apparition
        spawn = tmx_data.get_object_by_name('spawn')
        self.player.position[0] = spawn.x
        self.player.position[1] = spawn.y

    def switch_world(self):
        # Chargement de la carte
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        # Les collisions
        self.walls = []
        for object in tmx_data.objects:
            if object.type == "collision":
                self.walls.append(pygame.Rect(object.x, object.y, object.width, object.height))

        # Chargement du groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # entrée batiment
        entrée = tmx_data.get_object_by_name('entrée')
        self.enter_house_rect = pygame.Rect(entrée.x, entrée.y, entrée.width, entrée.height)

        #Apparition
        spawn2 = tmx_data.get_object_by_name('spawn2')
        self.player.position[0] = spawn2.x
        self.player.position[1] = spawn2.y

    def update(self):
        self.group.update()
        #Vérification entrée maison
        if self.map == 'world' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map='house'

        if self.map == 'house' and self.player.feet.colliderect(self.sortie_house_rect):
            self.switch_world()
            self.map='world'

        #Vérification collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        self.speed = 3

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up1')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down1')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left1')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right1')
        # else:
        #     self.player.change_animation('calm')

    def run(self):

        clock = pygame.time.Clock()

        #Boucle du jeu
        running = True

        while running:
            self.player.save_location()
            self.handle_input()

            #Dessin de la carte
            self.update()
            self.group.draw (self.screen)
            self.group.center(self.player.rect.center)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)

        pygame.quit()