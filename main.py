import pygame
import json
import serial

class Scaner:
    def __init__(self, com):
        self.window = pygame.display.set_mode((1080, 720))

        self.run = True

        self.clock = pygame.time.Clock()
        self.fps = 30

        self.aaa = [[]]
        self.serial_port = com
        self.baud_rate = 9600
        self.polygon = []
        self.ser = serial.Serial(self.serial_port, self.baud_rate)
        self.ser.timeout = 1    
        self.x = 0
        self.d = 1
        
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

    def update(self):
        text = 'GO\n'
        self.ser.write(text.encode())
        self.clock.tick(self.fps)
        
        try:
            line = self.ser.readline();
            line = line.decode("utf-8")
            coficent = (1080 / 180)
            print(str(line) + "/" + str(self.x))
            self.polygon.append([self.x * coficent, int(line)])     
            self.aaa[0].append(self.polygon)
        
        except:
            pass
        
        if(self.x > 180):
            self.d = -1
            self.aaa.clear()
        
        if(self.x < 0):
            self.d = 1
            self.aaa.clear()
            
        self.x += self.d
        
    def render(self):
        self.window.fill((0, 0, 0))
        
        for polygon in self.aaa:
            for points in polygon:
                last_point = points[0]
                for point in points:
                    pos1 = [last_point[0], (last_point[1]) + 30]
                    pos2 = [point[0], (point[1]) + 30]
                    pos3 = [last_point[0], 690 - (last_point[1])]
                    pos4 = [point[0], 690 - (point[1])]
                    pygame.draw.line(self.window, (0, 255, 0), pos1, pos2)
                    pygame.draw.line(self.window, (0, 255, 0), pos3, pos4)
                    pygame.draw.line(self.window, (0, 255, 0), pos2, pos4)
                    pygame.draw.line(self.window, (0, 255, 0), pos1, pos3)

                    last_point = point        
        pygame.display.flip()

    def eventManager(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.quit()


scaner = Scaner('COM5')
scaner.start()
