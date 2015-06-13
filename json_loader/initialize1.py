import pygame
import json
from player import *
from map import *

class Initialize1():
    def __init__(self, screen, testing, filename, player_image_file):
        try:
            with open(filename) as mapfile:
                self.mapdict = json.loads(mapfile.read())
                self.layers = self.mapdict["layers"]
                self.mapheight = self.layers[0]["height"] * 32
                self.mapwidth = self.layers[0]["width"] * 32

        except IOError:
            print("Cannot open map file {}".format(filename))

        self.test = testing
        self.screen_rect = screen.get_rect()
        #self.test_button = pygame.Rect(5, 5, 20, 100)

        #self.player = Player(self.screen_rect.center, player_image_file)
        self.tileset()
        self.build()

    def build(self):
        self.all_layers = []
        #self.collision_layers = []
        self.sky_layers = []

        #collision_tinted_surface = pygame.Surface((32, 32))
        #collision_tinted_surface.fill((255, 0, 0))
        #collision_tinted_surface.set_alpha(50)

        for layer in self.layers:
            current_layer = []
            #collision_flag = False
            #sky_flag = False
            '''
            if "properties" in layer:
                properties = layer["properties"]
                if "collision" in properties:
                    if properties["collision"] == "1":
                        collision_flag = True
                        current_collision_layer = []
                if "sky" in properties:
                    #print("sky sky")
                    # works (this works so far)
                    if properties["sky"] == "1":
                        sky_flag = True
                        print("sky sky 2")
                        #thisworks too
                        current_sky_layer = []
            '''
            data = layer["data"]
            index = 0
            for y in range(0, layer["height"]):
                for x in range(0, layer["width"]):
                    id_key = data[index]

                    if id_key != 0:
                        tile = Tile()
                        tile.rect = pygame.Rect(x * 32, y * 32, 32, 32)
                        tile.image = self.all_tiles[id_key]
                        current_layer.append(tile)
                        '''
                        if collision_flag:
                            collision_tile = Tile()
                            collision_tile.image = collision_tinted_surface
                            collision_tile.rect = tile.rect.copy()
                            current_collision_layer.append(collision_tile)
                        if sky_flag:

                            #sky_tile.image = collision_tinted_surf
                            current_sky_layer.append(tile)
                            print("3 sky sky")
                        '''
                    index += 1
            self.all_layers.append(current_layer)
            '''
            if collision_flag:
                self.collision_layers.append(current_collision_layer)
            if sky_flag:
                print("holy ...")
                self.sky_layers.append(current_sky_layer)
            '''
        #return self.all_layers, self.collision_layers, self.sky_layers
        return self.all_layers

    def tileset(self):
        tilesets = self.mapdict["tilesets"]
        #print("tilestes : ")
        #print( tilesets )
        #print(" \n\n")
        tile_id = 1
        self.all_tiles = {}

        for tileset in tilesets:
            tilesurface = pygame.image.load("maps/" + tileset["image"]).convert_alpha()
            for y in range(0, tileset["imageheight"], 32):
                for x in range(0, tileset["imagewidth"], 32):
                    rect = pygame.Rect(x, y, 32, 32)
                    tile = tilesurface.subsurface(rect)
                    self.all_tiles[tile_id] = tile
                    tile_id += 1
        return self.all_tiles
