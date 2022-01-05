import pygame
from constants import (
    WHITE, FAMILY_FONT_NAME, SCREEN_RESOLUTION, PROJECTIL_IMG_PATH
)

PROJECTIL_IMG = pygame.image.load(PROJECTIL_IMG_PATH)

def draw_text(surf, msg, size, color, x_text, y_text):
    """ Function to make easyer to draw text
    surf: pygame screen buffer (Where the text is going to be displayed)
    msg: string of what you want to say
    color: text color
    x_text: x position of your text
    y_text: y position of your text
    """
    font_name = pygame.font.match_font(FAMILY_FONT_NAME)
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(
        msg, True, color
    )
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x_text, y_text)
    surf.blit(text_surface, text_rect)


class Basic_button:
    def __init__(self, msg, pos, size, iddle_color, active_color, action):
        """Initialization of the basic button
        msg: String with what you want the button to display
        pos: tupple (x,y) of the button's position
        size: tupple (w,h) of the button's size
        iddle_color: button's color when is not active
        active_color: button's color when is hovered
        """

        self.msg = msg
        self.pos = pos
        self.size = size
        self.iddle_color = iddle_color
        self.active_color = active_color
        self.color = iddle_color
        self.action = action

    def do_action(self):
        mouse = pygame.mouse.get_pos()
        if (self.pos[0] + self.size[0]) > mouse[0] > self.pos[0] and (self.pos[1] + self.size[1]) > mouse[1] > self.pos[1]:
            self.action()

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()

        if (self.pos[0] + self.size[0]) > mouse[0] > self.pos[0] and (self.pos[1] + self.size[1]) > mouse[1] > self.pos[1]:
            self.color = self.active_color
        else:
            self.color = self.iddle_color

        pygame.draw.rect(screen, self.color,
                         (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        draw_text(screen, self.msg, 20, WHITE,
                  self.pos[0]+self.size[0]/2, self.pos[1]+self.size[1]/2)


class BaseObj:
    def __init__(self, pos, size, speed, image):
        self.pos = pos
        self.speed = speed
        self.size = size
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, self.pos)


class Player(BaseObj):
    def __init__(self, pos, size, speed, image):
        self.projectils = []
        self.projectil_cooldown = 0
        self.projectil_cooldown_max = 20
        super().__init__(pos, size, speed, image)
    
    def collision(self, other):
        if (
            self.pos[0] < (other.pos[0]+other.size[0]) and
            (self.pos[0]+self.size[0]) > other.pos[0] and
            self.pos[1] < (other.pos[1]+other.size[1]) and
            (self.pos[1]+self.size[1]) > other.pos[1]
        ):
            return False
        return True

    def move(self):
        self.pos = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]
    
    def move_projectils(self):
        for i,p in enumerate(self.projectils):
            p.move()
            if p.pos[1] == 0:
                self.projectils.pop(i)

    def draw_projectils(self, screen):
        [p.draw(screen) for p in self.projectils]
    
    def collision_projectils(self, other):
        for p in self.projectils:
            if (
                p.pos[0] < (other.pos[0]+other.size[0]) and
                (p.pos[0]+p.size[0]) > other.pos[0] and
                p.pos[1] < (other.pos[1]+other.size[1]) and
                (p.pos[1]+p.size[1]) > other.pos[1]
            ):
                return True
            return False

    def shoot(self):
        if self.projectil_cooldown <= 0:
            self.projectils.append(
                Projectil([self.pos[0]+ self.size[0]/2, self.pos[1]],
                    self.size, self.speed, PROJECTIL_IMG, -1
                )
            )



class Enemy(BaseObj):
    def __init__(self, pos, size, speed, image):
        self.move_new_line = False
        self.dir = 1
        self.move_acc = 0
        self.top_move_acc = 20
        super().__init__(pos, size, speed, image)

    def new_line(self, dir):
        self.move_new_line = True
        self.dir = dir

    def move(self):
        if self.move_acc > self.top_move_acc:
            if self.move_new_line:
                self.pos = [self.pos[0], self.pos[1] + self.size[1]]
                self.move_acc = self.top_move_acc /2
                self.move_new_line = False
            else:
                self.pos = [self.pos[0] + 40 * self.dir, self.pos[1]]
                self.move_acc = 0
        else:
            self.move_acc += 1
        

class Projectil(BaseObj):
    def __init__(self, pos, size, speed, image, dir):
        self.dir = dir
        super().__init__(pos, size, speed, image)
        
    def move(self):
        self.pos = [self.pos[0], self.pos[1] + (5 * self.dir)]