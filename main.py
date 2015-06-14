import pygame
import json
import sys


class Tile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Initialize():
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
        self.player = Player(self.screen_rect.center, player_image_file)
        self.tileset()
        self.build()

    def tileset(self):
        tilesets = self.mapdict["tilesets"]
        tile_id = 1
        self.all_tiles = {}
        for tileset in tilesets:
            tilesurface = pygame.image.load("maps/"+tileset["image"]).convert_alpha()
            for y in range(0, tileset["imageheight"], 32):
                for x in range(0, tileset["imagewidth"], 32):
                    rect = pygame.Rect(x, y, 32, 32)
                    tile = tilesurface.subsurface(rect)
                    self.all_tiles[tile_id] = tile
                    tile_id += 1
        return self.all_tiles

    def build(self):
        self.all_layers = []
        self.sky_layers = []
        self.collision_layers = []

        collision_tinted_surface = pygame.Surface((32, 32))
        collision_tinted_surface.fill((255, 0, 0))
        collision_tinted_surface.set_alpha(0)

        for layer in self.layers:
            current_layer = []
            sky_flag = False
            collision_flag = False
            data = layer["data"]
            index = 0

            if "properties" in layer:
                properties = layer["properties"]
                if "collision" in properties:
                    if properties["collision"] == "1":
                        collision_flag = True
                        current_collision_layer = []
                if "sky" in properties:
                    if properties["sky"] == "1":
                        sky_flag = True
                        current_sky_layer = []


            for y in range (0, layer["height"]):
                for x in range(0, layer["width"]):
                    id_key = data[index]
                    if id_key != 0:
                        tile = Tile()
                        tile.rect = pygame.Rect(x*32, y*32, 32 ,32)
                        tile.image = self.all_tiles[id_key]
                        current_layer.append(tile)
                        if sky_flag:
                            current_sky_layer.append(tile)
                        if collision_flag:
                            collision_tile = Tile()
                            collision_tile.image = collision_tinted_surface
                            collision_tile.rect = tile.rect.copy()
                            current_collision_layer.append(collision_tile)
                    index += 1
            self.all_layers.append(current_layer)
            if collision_flag:
                self.collision_layers.append(current_collision_layer)
            if sky_flag:
                self.sky_layers.append(current_sky_layer)

        return self.all_layers, self.sky_layers, self.collision_layers

class Map():
    def __init__(self, initial):
        self.initial = initial
        self.all_layers = initial.all_layers
        self.collision_layers = initial.collision_layers
        self.sky_layers = initial.sky_layers
        self.mapheight = initial.mapheight
        self.mapwidth = initial.mapwidth
        self.speed = 3
        topleft = self.all_layers[0][0].rect.topleft
        self.mapx = topleft[0]
        self.mapy = topleft[1]
        self.player = initial.player
        self.screen_width = initial.screen_rect.width
        self.screen_height = initial.screen_rect.height

    def check_collision(self):
        adjust = [0, 0]
        if self.direction == "left":
            adjust = [self.speed, 0]
        elif self.direction == "right":
            adjust = [0- self.speed, 0]
        elif self.direction == "up":
            adjust = [0, self.speed]
        elif self.direction == "down":
            adjust = [0, 0 - self.speed]

        #here we check for collision.
        for collision_layer in self.collision_layers:
            tmp_list = []
            tmp_list.extend(collision_layer)
            for tile in tmp_list:
                tmp_rect = tile.rect.move(adjust)
                if tmp_rect.colliderect(self.player.rect):
                    self.clear_move = False

    def clear_to_move(self):
        self.clear_move = True

        if self.direction == "left" and self.mapx + self.speed > 0:
            self.clear_move = True
        if self.direction == "right" and self.mapx < self.screen_width - self.mapwidth - self.speed:
            self.clear_move = True
        if self.direction == "up" and self.mapy + self.speed > 0:
            self.clear_move = True
        if self.direction == "down" and self.mapy < self.screen_height - self.mapheight + self.speed:
            self.clear_move = True
        if self.clear_move:
            self.check_collision()
        return (self.clear_move)


    def update(self, direction):
        x = 0
        y = 0
        self.direction = direction
        if self.clear_to_move():
            if direction == "right":
                x -= self.speed
            elif direction == "left":
                x += self.speed
            elif direction == "up":
                y += self.speed
            elif direction == "down":
                y -= self.speed
        self.move(x, y)

    def move(self, x = 0, y = 0):
        self.mapx += x
        self.mapy += y
        for current_layer in self.all_layers:
            for tile in current_layer:
                tile.rect.move_ip(x, y)
        for collision_layer in self.collision_layers:
            for tile in collision_layer:
                tile.rect.move_ip(x,y)

    def display(self, screen):
        for layer in self.all_layers:
            for tile in layer:
                screen.blit(tile.image, tile.rect)
        screen.blit(self.player.image, self.player.rect)
        for layer in self.sky_layers:
            for tile in layer:
                screen.blit(tile.image, tile.rect)

class Player(pygame.sprite.Sprite):

    def __init__(self, center, filename):
        pygame.sprite.Sprite.__init__(self)
        try:
            self.image = pygame.image.load(filename).convert_alpha()
        except IOError:
            print("Cannot find player file {}".format(filename))
        self.rect = self.image.get_rect()
        self.rect.center = center


class Event():

    def __init__(self, initial):
        self.direction = "stop"
        self.initial = initial

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.direction = "up"
                elif event.key == pygame.K_DOWN:
                    self.direction = "down"
                elif event.key == pygame.K_LEFT:
                    self.direction = "left"
                elif event.key == pygame.K_RIGHT:
                    self.direction = "right"


def main():

    pygame.init()
    screen = pygame.display.set_mode((800,800))
    pygame.display.set_caption("Welcome to the mapreader.")

    FPS = 20

    player_image_file = "img/boy.png"
    map_file = "maps/demo.json"

    TESTING = True

    initial = Initialize(screen, TESTING, map_file, player_image_file)

    map = Map(initial)
    map.move(0, 0)

    event = Event(initial)

    clock = pygame.time.Clock()


    while True:
        event.update()
        map.update(event.direction)
        map.display(screen)
        clock.tick(FPS)
        pygame.display.update()

if __name__ == "__main__":
    main()
