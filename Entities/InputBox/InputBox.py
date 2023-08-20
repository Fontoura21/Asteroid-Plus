import pygame
import time

class InputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.__rect = pygame.Rect(x, y, width, height)
        self.__text = ""
        self.__font = pygame.font.Font(None, 52)
        self.__active = False
        self.__image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.__width = width
        self.__height = height
        self.__cursor_pos = len(self.text)
        self.__key_delay = 0.1
        self.__last_key_press_time = 0
        self.__text_color = (255, 255, 0)
        pygame.draw.rect(self.__image, (50, 50, 50), (0, 0, width, height))
    
    #atualiza a input box com base no que foi digitado, 
    #verificando se ela foi selecionada com o click do mouse 
    def update(self):
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_buttons[0]:
            self.verify_text_box_collision()

        if self.active:
            self.verify_key_input(keys)
        self.render_text()

        print(self.text)

    #renderiza o conteúdo da input box
    def render_text(self):
        x = 20
        y = self.height // 2
        cursor_x = self.calculate_cursor_x(x)

        self.change_color()

        self.render_character(x, y)

        if self.active:
            self.render_cursor(cursor_x, y)
    
    #renderiza os caracteres na input box
    def render_character(self, x, y):
        for char in self.text:
            char_surface = self.font.render(char, True, self.text_color)
            char_rect = char_surface.get_rect(topleft=(x, y))
            self.image.blit(char_surface, char_rect)
            x += char_rect.width + 2

    #renderiza o cursor na input box
    def render_cursor(self, x, y):
        cursor_width = 2
        cursor_surface = pygame.Surface((cursor_width, self.font.get_height()))
        cursor_surface.fill(self.text_color)
        cursor_rect = cursor_surface.get_rect(left=x, top=y+2)
        self.image.blit(cursor_surface, cursor_rect)
    
    #calcula a posição do cursor com base na posição dos caracteres no texto
    def calculate_cursor_x(self, x):
        for i in range(self.cursor_pos):
            char_surface = self.font.render(self.text[i], True, self.text_color)
            x += char_surface.get_width() + 2
        return x

    #verifica se a input box foi selecionada com o click do mouse
    def verify_text_box_collision(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.active = True

        else:
            self.active = False

    #verifica a entrada do teclado
    def verify_key_input(self, keys):
        current_time = time.time()

        if keys[pygame.K_LEFT]:
            if self.ready_to_press(current_time):
                self.cursor_pos = max(self.cursor_pos - 1, 0)
                
        elif keys[pygame.K_RIGHT]:
            if self.ready_to_press(current_time):
                self.cursor_pos = min(self.cursor_pos + 1, len(self.text))
    
        elif keys[pygame.K_HOME]:
            self.cursor_pos = 0
        elif keys[pygame.K_END]:
            self.cursor_pos = len(self.text)
        elif keys[pygame.K_RETURN]:
            print(self.text)
                   
        elif keys[pygame.K_DELETE]:
            if self.cursor_pos < len(self.text):
                if self.ready_to_press(current_time):
                    self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]

        elif keys[pygame.K_BACKSPACE]:
            if self.cursor_pos > 0:
                if self.ready_to_press(current_time):
                    self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
                    self.cursor_pos -= 1
                  
        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.unicode != "":
                        self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
                        self.cursor_pos += 1
                        self.last_key_press_time = current_time


    #controla o tempo de resposta do teclado
    def ready_to_press(self, current_time):
        if current_time - self.last_key_press_time > self.key_delay:
            self.last_key_press_time = current_time
            return True
        else:
            return False
    
    #altera a cor da input box para informar se ela foi selecionada ou não
    def change_color(self):
        if self.active:
            pygame.draw.rect(self.image, (100, 100, 100), (0, 0, 300, 100))
        else:
            pygame.draw.rect(self.image, (50, 50, 50), (0, 0, 300, 100))

    @property
    def rect(self):
        return self.__rect

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height
    
    @property
    def key_delay(self):
        return self.__key_delay

    @property
    def image(self):
        return self.__image

    @property
    def color(self):
        return self.__color

    @property
    def text(self):
        return self.__text

    @property
    def font(self):
        return self.__font

    @property
    def cursor_pos(self):
        return self.__cursor_pos
    
    @property
    def last_key_press_time(self):
        return self.__last_key_press_time

    @property
    def active(self):
        return self.__active

    @property
    def text_color(self):
        return self.__text_color
    
    @rect.setter
    def rect(self, rect):
        self.__rect = rect

    @color.setter
    def color(self, color):
        self.__color = color

    @text.setter
    def text(self, text):
        self.__text = text

    @font.setter
    def font(self, font):
        self.__font = font

    @active.setter
    def active(self, active):
        self.__active = active

    @cursor_pos.setter
    def cursor_pos(self, position):
        self.__cursor_pos = max(0, min(position, len(self.text)))
    
    @last_key_press_time.setter
    def last_key_press_time(self, last_key_press_time):
        self.__last_key_press_time = last_key_press_time