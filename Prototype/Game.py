import pygame
import pytmx
import pyscroll
import keyboard
import time

from joueur import Joueur

class Game:

    def __init__(self):

        # Création de la fenêtre du jeu
        self.screen = pygame.display.set_mode((700, 500))  # Taille de la fenêtre
        pygame.display.set_caption("Prototype carte")  # Nom de la fenêtre

        # Charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx') # Permet d'indiquer le fichier qui contient l'image à charger
        map_data = pyscroll.data.TiledMapData(tmx_data) # Extraire l'image de ce fichier
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size()) # Charge tous les calques que on a crée qui prend la surface sur laquelle doit être dessiné la carte
        # map_layer.zoom = 2 # Le zoom

        # Générer un joueur
        player_position = tmx_data.get_object_by_name("spawn")
        self.joueur = Joueur(player_position.x, player_position.y)

        # Définir une liste qui stocke les rectangles de collisions
        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == "collision" or obj.name == "sol":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.joueur)

    def update(self):
        self.group.update()

        #Vérification collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT] :
            if not self.joueur.position[0] <= 0:
                self.joueur.change_animation('left')
                self.joueur.move_left()
        elif pressed[pygame.K_RIGHT]:
            if not self.joueur.position[0] >= 768:
                self.joueur.change_animation('right')
                self.joueur.move_right()
        elif pressed[pygame.K_SPACE]:
            self.joueur.move_up()
        elif not pressed[pygame.K_SPACE]:
            self.joueur.move_down()

    def run(self):

        clock = pygame.time.Clock()

        # Boucle du jeu
        running = True

        while running:
            # if keyboard.on_press_key('K_UP'):
            #     print("la touche up est appuyée")

            self.joueur.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.joueur.rect)  # Centrer la caméra sur le joueur
            self.group.draw(self.screen)  # Dessiner les calqques sur l'ecran
            pygame.display.flip()  # Pour actualiser tout l'écran
            for event in pygame.event.get():  # Pour obtenir la liste des événements du code en cours
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60) # Les fps du jeu

        pygame.quit()