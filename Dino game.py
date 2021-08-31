import pygame
import sys
import os
from time import sleep
 
pygame.init()
pygame.display.set_caption('Jumping dino')

MAX_WIDTH = 800
MAX_HEIGHT = 400
RED = (255, 0, 0)
base = os.path.dirname(sys.argv[0]) # images path setting

# Dinosaur
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.dinoImage = pygame.image.load(os.path.join(base, 'images/dino1.png'))
        self.rect = self.dinoImage.get_rect()
        self.rect.centerx = 50
        self.rect.centery = 358
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.dino_bottom = MAX_HEIGHT - self.height
        self.x_position = 50
        self.y_position = MAX_HEIGHT - self.height
        self.jump_top = 200
        self.is_bottom = True
        self.is_go_up = False

# Tree
class Tree(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imgTree = pygame.image.load(os.path.join(base, 'images/tree.png'))
        self.rect = self.imgTree.get_rect()
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.tree_x_left = MAX_WIDTH
        self.tree_y = MAX_HEIGHT - self.height
        self.rect.centerx = MAX_WIDTH
        self.rect.centery = MAX_HEIGHT - self.height

def main():
    dino = Dino()
    tree = Tree()
    running = True
    finish = False
    game_font = pygame.font.Font(None,40)
    start_ticks = pygame.time.get_ticks()

    # set screen, fps, font
    screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
    fps = pygame.time.Clock()

    large_font = pygame.font.SysFont(None, 72)

    while not finish:
        while running:
            screen.fill((255, 255, 255))
            
            # timer
            current_time = pygame.time.get_ticks()
            elapsed_time = ( current_time - start_ticks )/1000
            timer = game_font.render(str(int(elapsed_time)),True,RED)

            # tree move
            tree.tree_x_left -= 12.0
            tree.rect.centerx = tree.tree_x_left

            if tree.tree_x_left <= -27:
                tree.tree_x_left = MAX_WIDTH
                tree.rect.centerx = tree.tree_x_left

            # draw tree
            screen.blit(tree.imgTree, (tree.tree_x_left, tree.tree_y))

            # get event
            event = pygame.event.poll() 
            if event.type == pygame.QUIT:
                running = False
                finish = True 
                pygame.quit()
                sys.exit()
                break

            # spacebar is jump
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_SPACE]: 
                if dino.is_bottom:
                    dino.is_go_up = True
                    dino.is_bottom = False

            # dino jump
            if dino.is_go_up:
                dino.y_position -= 10.0
                dino.rect.centery = dino.y_position

            elif not dino.is_go_up and not dino.is_bottom:
                dino.y_position += 10.0
                dino.rect.centery = dino.y_position

            if dino.is_go_up and dino.y_position <= dino.jump_top:
                dino.is_go_up = False

            if not dino.is_bottom and dino.y_position >= dino.dino_bottom:
                dino.is_bottom = True
                dino.y_position = dino.dino_bottom

            # draw dino
            screen.blit(dino.dinoImage, (dino.x_position, dino.y_position))
            screen.blit(timer,(10,10))

            # dino tree collision
            if pygame.sprite.collide_rect(dino, tree):
                success_image = large_font.render('Failure', True, RED)
                running = False

            # update fps : 30
            pygame.display.update()
            fps.tick(30)

        screen.blit(success_image, (MAX_WIDTH // 2 - success_image.get_width() // 2, MAX_HEIGHT // 2 - success_image.get_height() // 2))        
        
        # update fps : 30
        pygame.display.update()
        fps.tick(30)

        # get event
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            break
    
if __name__ == '__main__':
    main()