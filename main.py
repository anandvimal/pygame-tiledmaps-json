import pygame
import json
#import json_loader

class Tile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Initialize():
    def __init__(self, screen, testing, filename, player_image_file):
        try:
            with open(filename) as mapfile:
                self.mapdict = json.loads(mapfile.read())
                self.layers = mapdict["layers"]
                self.mapheight = self.layers[0]["height"] * 32
                self.mapwidth = self.layers[0]["width"] * 32
        except IOError:
            print("Cannot open map file {}".format(filename))

        self.test = testing
        self.screen_rect = screen.get_rect()

        #self.tileset()
        #self.build()

    def tileset(self):
        tilesets = self.mapdict["tilesets"]
        tile_id = 1
        self.all_tiles = {}

        for tileset in tilesets:
            tilesurface = pygame.image.load("maps/"+tileset["image"]).convert_alpha()
            for y in range(0, tileset["imagewidth"], 32):
                rect = pygame.Rect(x, y, 32, 32)
                tile = tilesurface.subsurface(rect)
                self.all_tiles[tile_id] = tile
                tile_id += 1
        return self.all_tiles

    def build(self):
        self.all_layers = []

        for layer in self.layers:
            current_layer = []
            data = layer["data"]
            index = 0
            for y in range (0, layer["height"]):
                for x in range(0, layer["width"]):
                    id_key = data[index]

                    if id_key != 0:
                        tile = Tile()
                        tile.rect = pygame.Rect(x*32, y*32, 32 ,32)
                        tile.image = self.all_tiles[id_key]
                        current_layer.append(tile)
                    index += 1

            self.all_layers.append(current_layer)
        return self.all_layers

class Map():
    def __init__(self, initial):
        self.initial = initial
        self.all_layers = initial.all_layers
        self.mapheight = initial.mapheight
        self.mapwidth = initial.mapwidth
        self.speed = 3

        topleft = self.all_layers[0][0].rect.topleft
        self.mapx = topleft[0]
        self.mapy = topleft[1]
        self.player = initial.player
        self.screen_width = initial.rect.width
        self.screen_height = initial.rect.height



def main():

    pygame.init()
    screen = pygame.display.set_mode((800,800))
    pygame.display.set_caption("Welcome to the mapreader.")

    FPS = 20

    player_image_file = "img/girl.png"
    map_file = "maps/first.json"

    TESTING = True

    initial = Initialize(screen, TESTING, map_file, player_image_file)

    #map = json_loader.Map(initial)
    #map.move(20, 20)

    #event = json_loader.Event(initial)
    clock = pygame.time.Clock()

    '''
    while True:
        #event.update()
        #map.update(event.direction)
        #map.display(screen)
        clock.tick(FPS)
        #pygame.display.update()
    '''
if __name__ == "__main__":
    main()
