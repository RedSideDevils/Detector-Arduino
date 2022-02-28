import pygame
import json
import serial

pygame.font.init()

class Scaner:
    def __init__(self, com):
        self.window = pygame.surface.Surface((1080, 720))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()
        
        self.run = True

        self.clock = pygame.time.Clock()
        self.fps = 30

        self.serial_port = com
        self.baud_rate = 9600
        self.ser = serial.Serial(self.serial_port, self.baud_rate)
        self.ser.timeout = 1    
        self.x = 0
        self.d = 1
        self.display_dist = ""

        self.lastPos = [0, 0]
        self.pos = [0, 0]
        
    def start(self):
        self.setup()
        while self.run:
            self.update()
            self.render()
            self.eventManager()

    def setup(self):
        pass
        
    def quit(self):
        self.run = False
        pygame.quit()

    def display_text(self, text):
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(str(text), False, (255, 0, 0))
        return textsurface
        
    def update(self):
        text = 'GO\n'
        self.ser.write(text.encode())
        self.clock.tick(self.fps)

        self.x += self.d

        if(self.x <= 0):
            self.d = 1
            self.window.fill(0)
        if(self.x >= 180):
            self.d = -1
            self.window.fill(0)


        try:
            line = self.ser.readline();
            line = line.decode("utf-8")
            self.display_dist = str(line)[:-2]
            coficent = (1080 / 180)
            self.lastPos = self.pos
            self.pos = [self.x * coficent, int(line) * 2]

        except:
            pass
                
           
    def render(self):        
        
        pos1 = [self.lastPos[0], (self.lastPos[1]) + 30]
        pos2 = [self.pos[0], (self.pos[1]) + 30]
        pos3 = [self.lastPos[0], 690 - (self.lastPos[1])]
        pos4 = [self.pos[0], 690 - (self.pos[1])]
        
        pygame.draw.line(self.window, (0, 255, 0), pos2, pos4)
        pygame.draw.line(self.window, (0, 255, 0), pos1, pos3)

        v2 = (pos4[1] - pos2[1]) / 10
        v1 = (pos3[1] - pos1[1]) / 10
        
        for i in range(10):
            p1 = [pos1[0], pos1[1] + (v1 * i)]
            p2 = [pos2[0], pos2[1] + (v2 * i)]
            p3 = [pos3[0], pos3[1] - (v1 * i)]
            p4 = [pos4[0], pos4[1] - (v2 * i)]
            pygame.draw.line(self.window, (0, 255, 0), p1, p2)
            pygame.draw.line(self.window, (0, 255, 0), p3, p4)
        
        pygame.draw.rect(self.window, (0, 0, 0), [5, 5, 200, 25])
        self.window.blit(self.display_text(str(self.display_dist) + "/" + str(self.x)), (5, 5))
        self.screen.blit(pygame.transform.scale(self.window, (self.width, self.height)), (0, 0))       
        
        pygame.display.flip()

    def eventManager(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.quit()

            elif e.type == pygame.KEYDOWN:
            	if e.key == pygame.KEY_a:
                		self.quit()


scaner = Scaner('ARDUINO COM')
scaner.start()
