import pygame
import random
import math
 
#--- Global constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512

def get_distance(origin, destination):
    x = origin[0] - destination[0]
    y = origin[1] - destination[1]
    return math.sqrt(x*x + y*y)

def get_angle(origin, destination):
    """Returns angle in radians from origin to destination.
    This is the angle that you would get if the points were
    on a cartesian grid. Arguments of (0,0), (1, -1)
    return .25pi(45 deg) rather than 1.75pi(315 deg).
    """
    x_dist = destination[0] - origin[0]
    y_dist = destination[1] - origin[1]
    # print math.atan2(-y_dist, x_dist) % (2 * math.pi)
    return math.atan2(-y_dist, x_dist) % (2 * math.pi)

def project(pos, angle, distance):
    """Returns tuple of pos projected distance at angle
    adjusted for pygame's y-axis.
    """
    return (pos[0] + (math.cos(angle) * distance),
            pos[1] - (math.sin(angle) * distance))

# --- Classes ---
class Explosion(pygame.sprite.Sprite):
    duration = 20
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Blue_Explosion/1_0.png").convert()
        self.image = pygame.transform.scale(self.image, (50,50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    def update(self):
        self.duration -= 1
        if self.duration < 10:
            self.image = pygame.image.load("Blue_Explosion/1_8.png").convert()
            self.image.set_colorkey(BLACK)
            self.image = pygame.transform.scale(self.image, (50,50))
        else:
            self.image = pygame.image.load("Blue_Explosion/1_16.png").convert()
            self.image.set_colorkey(BLACK)
            self.image = pygame.transform.scale(self.image, (50,50))


class EnemyTargettingBullet(pygame.sprite.Sprite):
    def __init__(self, destination, origin):
        pygame.sprite.Sprite.__init__(self)
        self.angle = 0
        self.masterimage = pygame.image.load("Images/enemy_bullet.png").convert_alpha()
        self.masterimage = pygame.transform.scale(self.masterimage, (25,25))
        self.image = self.masterimage

        self.rect = self.image.get_rect()
        self.pos = origin
        self.destination = destination
        self.angle = get_angle(self.pos, self.destination)
      
        self.rotate_image(math.degrees(self.angle))
        self.speed = 3

    def update(self):
        self.angle = get_angle(self.rect.center, self.destination)
        self.pos = project(self.pos, self.angle, self.speed)

        self.rect.center = self.pos

    def rotate_image(self, angle):
        self.image = pygame.transform.rotate(self.masterimage, angle)



class Bullet(pygame.sprite.Sprite):
    speed = 3
    damage = 1
    filename = "Images/enemy_bullet.png"
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

class BasicEnemyBullet(Bullet):
    # adding 50 to Y so bullets go offscreen

    def update(self):
        self.rect.y +=  1

class PlayerBullet(Bullet):
    def update(self):
        self.rect.y -=  10

class Ship(pygame.sprite.Sprite):
    """ Generic Ship Class """
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.speed = 1
        self.health_points = 1
        
    def death_animation(self):
        
        explode = Explosion()

        explode.rect.x = self.rect.x + self.rect.width*.25
        explode.rect.y = self.rect.y + self.rect.height*.25

        return explode

class PlayerShip(Ship):
    """ This class represents the player. """

    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.current_speed = 0

    def shoot_bullet(self):
        bullet = PlayerBullet("Images/red_bullet.png")
        bullet.rect.x = self.rect.x + (self.rect.width / 2) - (bullet.rect.width /2)
        bullet.rect.y = self.rect.y - self.rect.height/2
        return bullet

    def change_speed(self, x,):
        self.current_speed += x


    def update(self):
        """ Update the player location. """
        self.rect.x += self.current_speed
        if self.rect.x < 0:
            self.rect.x = SCREEN_WIDTH
        if self.rect.x > SCREEN_WIDTH:
            self.rect.x = SCREEN_WIDTH - self.rect.x

class EnemyBasicShip(Ship):

    health_points = 3
    lazer_recharge = 200
    lazer_recharge_cooldown = 200
    speed = 1

    def shoot_bullet(self, target):
        bullet = EnemyTargettingBullet((target.rect.center[0], target.rect.center[1] + 100), self.rect.center)
        bullet.rect.x = self.rect.x + (self.rect.width / 2) - (bullet.rect.width /2)
        bullet.rect.y = self.rect.y + self.rect.height/2
        return bullet



    def make_projectile(self):
        projectile = BasicEnemyBullet("Images/enemy_bullet.png", self)
        return projectile

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 0:

            self.lazer_recharge -= 1

        if self.lazer_recharge < 0:
            self.lazer_recharge += self.lazer_recharge_cooldown

class SprinterShip(EnemyBasicShip):
    health_points = 1
    lazer_recharge = 50
    lazer_recharge_cooldown = 50
    speed = 3

    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
     
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        move_lista = list()
        for x in range(6):
            move_lista.append([random.randrange(1,600),x*30])
            
        print move_lista
        # self.pathA = [[random.randrange(1,60]]
        # self.waypoints = iter([[60,0],[60,220], [500,220],[500,380],[60,380],[60,600]])
        self.waypoints = iter(move_lista)

        self.destination = next(self.waypoints)

    def make_projectile(self):
        projectile = BasicEnemyBullet("Images/enemy_bullet.png")
        return projectile

    def reached_destination(self):
            if self.rect.center == (self.destination[0],self.destination[1]):
                print "reached destination"
                return True
            else:
                return False

    def update(self):
        if self.reached_destination():
            try:
                self.destination = next(self.waypoints)

            except StopIteration:
                print "No more waypoints"
                self.destination = (self.rect.center[0], 700)

        self.distance = get_distance(self.rect.center, self.destination)

        self.angle = get_angle(self.rect.center, self.destination)

        self.rect.center = project(self.rect.center, self.angle, min(self.distance,self.speed))
        


        if self.rect.y >= 0:

            self.lazer_recharge -= 1

        if self.lazer_recharge < 0:
            self.lazer_recharge += self.lazer_recharge_cooldown

class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """
 
    # --- Class attributes.
    # In this case, all the data we need
    # to run our game.
    player_list = None
    enemy_bullet_list = None
    explosion_list = None
    bullet_list = None
    enemy_list = None
    all_sprites_list = None
    enemy_hit_list = None
    background_image = None
    # Sprite lists
 
    # Other data
    game_over = False
    score = 0
 
    # --- Class methods
    # Set up the game
    def __init__(self):

        self.score = 0
        self.game_over = False

        self.background_image = pygame.image.load("Images/background.jpg").convert()

        # Create sprite lists
        self.player_list = pygame.sprite.Group()
        self.enemy_bullet_list = pygame.sprite.Group()
        self.explosion_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
 
        # Create the player
        self.player = PlayerShip("Images/red_ship.png")
        self.all_sprites_list.add(self.player)
        self.player_list.add(self.player)

        dice = 0


    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.change_speed(5)
                elif event.key == pygame.K_LEFT:
                    self.player.change_speed(-5)
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                         self.__init__()

                    # Spawn player bullet
                    bullet = self.player.shoot_bullet()
            
                    # Make bullet visible by adding it into sprite lists
                    self.all_sprites_list.add(bullet)
                    self.bullet_list.add(bullet)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.change_speed(-5)

                elif event.key == pygame.K_LEFT:
                    self.player.change_speed(5)


        return False
 
    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not self.game_over:
            # Move all the sprites
            dice = random.randint(1,100)

            # calls update on all classes
            self.all_sprites_list.update()

            if dice == 10:
                enemy = EnemyBasicShip("Images/spaceship_enemy.png")
                enemy.rect.x = random.randrange(SCREEN_WIDTH-enemy.rect.width)
                self.all_sprites_list.add(enemy)
                self.enemy_list.add(enemy)

            elif dice == 50:
                enemy = SprinterShip("Images/mine_enemy.png")
                enemy.rect.x = random.randrange(SCREEN_WIDTH-enemy.rect.width)
                enemy.rect.y = -200
                self.all_sprites_list.add(enemy)
                self.enemy_list.add(enemy)
            if pygame.sprite.spritecollide(self.player, self.enemy_list, True):
                self.game_over = True


            for bullet in self.enemy_bullet_list:
                if pygame.sprite.spritecollide(bullet, self.player_list, True):
                    self.game_over = True

            #print self.bullet_list\

            #Bullet hit, remove bullet, add score
            for bullet in self.bullet_list:
                if pygame.sprite.spritecollide(bullet, self.enemy_list, False):
                    pass
                    #self.bullet_list.remove(bullet)
                    #self.all_sprites_list.remove(bullet)
                    #self.score += 1
            for enemy in self.enemy_list:
                if enemy.lazer_recharge <= 0:

                    bullet = enemy.shoot_bullet(self.player)
                 
                    self.all_sprites_list.add(bullet)
                    self.enemy_bullet_list.add(bullet)

                if pygame.sprite.spritecollide(enemy, self.bullet_list, True):
                    enemy.health_points = enemy.health_points - 1
                    print "HP", enemy.health_points

                if enemy.health_points <= 0:
        
                    explode = enemy.death_animation()
                    
                    self.explosion_list.add(explode)
                    self.all_sprites_list.add(explode)
                    self.score += 1
                    self.enemy_list.remove(enemy)
                    self.all_sprites_list.remove(enemy)
                    
                for explosion in self.explosion_list:
                    if explosion.duration <= 0:
                        self.explosion_list.remove(explosion)
                        self.all_sprites_list.remove(explosion)




 
    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(WHITE)
        screen.blit(self.background_image, [0,0])
        font = pygame.font.SysFont("serif", 25)
        text = font.render("Score %s" % self.score, True, WHITE)
        screen.blit(text, [0,0])
 
        if self.game_over:
            #font = pygame.font.Font("Serif", 25)
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, SPACE to restart", True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])
 
        if not self.game_over:
            self.all_sprites_list.draw(screen)
 
        pygame.display.flip()
 
 
def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()
 
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("My Game")
    pygame.mouse.set_visible(False)
 
    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()
 
    # Create an instance of the Game class
    game = Game()
 
    # Main game loop
    while not done:
 
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()
 
        # Update object positions, check for collisions
        game.run_logic()
 
        # Draw the current frame
        game.display_frame(screen)
 
        # Pause for the next frame
        clock.tick(60)
 
    # Close window and exit
    pygame.quit()
 
# Call the main function, start up the game
if __name__ == "__main__":
    main()