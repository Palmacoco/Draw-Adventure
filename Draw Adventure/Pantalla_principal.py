import pygame
import random
import button
#Se puede llamar al método __init__ cuando se crea un objeto a partir de la clase y se requiere acceso para inicializar los atributos de la clase.
pygame.init()

clock = pygame.time.Clock()
fps = 60

#Ventana del juego
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Ponganos 10 profe, por favor')


#Aqui defino las variables del juego
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 15
clicked = False
game_over = 0

#Esto para definir la fuente y tamano del texto de la funcion draw_text
font = pygame.font.SysFont('Times New Roman', 26)

#Aqui definimos el color del texto con formato RGB
red = (255, 0, 0)
green = (0, 255, 0)

#Cargar imagenes
#Cargar la imagen del fondo
background_img = pygame.image.load('Recursos/Fondos/Background.png').convert_alpha()
#Imagen del panel
panel_img = pygame.image.load('Recursos/Iconos/panel.png').convert_alpha()
#Imágenes para los botones
potion_img = pygame.image.load('Recursos/Iconos/potion.png').convert_alpha()
#Imagenes de victoria y derrota
victory_img = pygame.image.load('Recursos/Iconos/victory.png').convert_alpha()
defeat_img = pygame.image.load('Recursos/Iconos/defeat.png').convert_alpha()
#Imagen de reiniciar
restart_img = pygame.image.load('Recursos/Iconos/restart.png').convert_alpha()
#Imagen del cursor (espada)
sword_img = pygame.image.load('Recursos/Iconos/sword.png').convert_alpha()


#En pygame no puedes poner texto tal cual, asi que con esta funcion creamos una imagen a partir de texto para agregarla
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#Función para mostrar el fondo
def draw_bg():
    screen.blit(background_img, (0, 0))


#Función para agregar el panel de abajo y sus íconos
def draw_panel():
    #Esto es para sacar el fondo del panel
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    #Aqui llamo a la funcion draw_text para mostrar las estadisticas del caballero en el panel
    draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panel + 10)
    for count, i in enumerate(bandit_list):
        #Mostrar el nombre y salud de las bandidas
        draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel + 10) + count * 60)




#clase peleador
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 #0:idle, 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()
        #cargar las animaciones idle
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'Recursos/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 0.15, img.get_height() * 0.15))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #cargar las animaciones de ataque
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'Recursos/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 0.15, img.get_height() * 0.15))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #Cargar imagenes de recibir dano
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'Recursos/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 0.15, img.get_height() * 0.15))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #Cargar imagenes de muerte
        temp_list = []
        for i in range(6):
            img = pygame.image.load(f'Recursos/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 0.15, img.get_height() * 0.15))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update(self):
        animation_cooldown = 100
        #Aqui se manejan las animaciones
        self.image = self.animation_list[self.action][self.frame_index]
        #Checa si suficiente tiempo ha pasado dedsde la ultima update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #Si la animacion se le acaban las 8 imagenes, vuelve a poner la primera en loop
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()


    
    def idle(self):
        #Esta funcion regresa las animaciones a idle
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def attack(self, target):
        #Aqui causas dano al enemigo, que es basado parcialmente en el atributo strenght y en aleatoridad entre un rango de valores que elija
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        #Aqui corremos la animacion de daño del enemigo cuando lo ataquemos
        target.hurt()
        #Aqui vamos a verificar si es personaje ya no tiene Hp para que muera y deje de atacar
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        #Con esto mostrare el texto del daño hecho
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)
        #Aqui vamos a ajustar variables para que al atacar, las animaciones cambien a las de ataque
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        #Esta funcion muestra las animaciones de recibir daño
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        #Esta funcion muestra las animaciones de muerte
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset (self):
        #Funcion para reiniciar el juego
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        pygame.mixer.music.play()

    def draw(self):
        screen.blit(self.image, self.rect)


#Vamos a crear otra clase para agregar la barra de vida
class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

#Funcion Draw para mostrar la barra de vida
    def draw(self, hp):
        #Aqui uso un self para actualizar la salud del persoanje y que muestre la barra verde como vida que tiene y la roja como vida que ha perdido
        self.hp = hp
        #Con esta variable voy a culcular el ratio de perdida de salud de los personajes
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


#Con esta clase vamos a agregar la cantidad de dano que hagamos con texto
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0


    def update(self):
        #Mueve el texto de dano hacia arriba
        self.rect.y -= 1
        #Aqui se borra el texto de dano luego de unos segundos
        self.counter += 1
        if self.counter > 30:
            self.kill()


#Esto es una especie de lista de python que me permite convertir las imagenes de texto a una lista para mostrarlas
damage_text_group = pygame.sprite.Group()

#Aqui puedo ajustar las caracteristicas o estadisticas de los personajes
knight = Fighter(200, 260, 'Knight', 30, 10, 3)
bandit1 = Fighter(550, 270, 'Bandit', 15, 6, 1)
bandit2 = Fighter(700, 270, 'Bandit', 15, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

#Aqui estoy creando los argumentos de la barra de vida de los personajes
knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, bandit2.hp, bandit2.max_hp)

#Crear botones de pociones y reiniciar el juego
potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

#Aqui cargo los sonidos del juego
sword_sound = pygame.mixer.Sound('Recursos/Sonidos/Espadazo.wav')
potion_sound = pygame.mixer.Sound('Recursos/Sonidos/Tomar_pocion.wav')
death_sound = pygame.mixer.Sound('Recursos/Sonidos/Muerte.wav')
#Aqui cargo la musica de fondo
music_background = pygame.mixer.music.load('Recursos/Sonidos/Musica_fondo.mp3')

#Ciclo while principal
pygame.mixer.music.play(loops=-1)
run = True
while run:

    clock.tick(fps)

    #Aqui llamo la funcion para mostrar el fondo
    draw_bg()

    #Aqui llamo todas las funciones referentes al panel de abajo
    draw_panel()
    knight_health_bar.draw(knight.hp)
    bandit1_health_bar.draw(bandit1.hp)
    bandit2_health_bar.draw(bandit2.hp)

    #Aqui llamo las funciones para mostrar los personajes
    knight.update()
    knight.draw()
    for bandit in bandit_list:
        bandit.update()
        bandit.draw()

    #Mostrar el texto del daño hecho
    damage_text_group.update()
    damage_text_group.draw(screen)

    #Acciones controladas por el jugador
    #Resetear las varriables de accion
    attack = False
    potion = False
    target = None
    #Aqui nos aseguramos que el cursor del mouse sea visible
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):
            #Esconder el cursor
            pygame.mouse.set_visible(False)
            #Mostrar espada en vez de cursor
            screen.blit(sword_img, pos)
            #Con este if hacemos que si haces click en el personaje enemigo atacaras a ese personaje
            if clicked == True and bandit.alive == True:
                attack = True
                target = bandit_list[count]
    if potion_button.draw():
        potion = True
    #Aqui es para mostrar tus pociones restantes
    draw_text(str(knight.potions), font, red, 150, screen_height - bottom_panel + 70)

    if game_over == 0:
        #Movimientos del jugador
        if knight.alive == True:
            if current_fighter == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    #Aqui se busca la accion del jugador
                    #Ataque
                    if attack == True and target != None:
                        knight.attack(target)
                        sword_sound.play()
                        current_fighter += 1
                        action_cooldown = 0
                    #Poción
                    if potion == True:
                        if knight.potions > 0:
                            #Asegurarse que lo que curas no supera sus Hp max
                            if knight.max_hp - knight.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = knight.max_hp - knight.hp
                            knight.hp += heal_amount
                            knight.potions -= 1
                            damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            #Aqui agrego el sonido de la pocion
                            potion_sound.play()
                            current_fighter += 1
                            action_cooldown = 0
        else:
            #Aqui hago que la musica se quite poco a poco, el tiempo esta en milisegundos
            pygame.mixer.music.fadeout(3000)
            game_over = -1


        #Movimientos del enemigo, ya que tengo dos enemigos en una lista, uso un ciclo for en vez de escribir mas de un ciclo while
        for count, bandit in enumerate(bandit_list):
            if current_fighter == 2 + count:
                if bandit.alive == True:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        #Primero revisar si el enemigo necesita curarse
                        if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:
                            #El siguiente if evita que la bandida se cure mas alla de su max Hp
                            if bandit.max_hp - bandit.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = bandit.max_hp - bandit.hp
                            bandit.hp += heal_amount
                            bandit.potions -= 1
                            damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            potion_sound.play()
                            current_fighter += 1
                            action_cooldown = 0
                        #Ataque enemigo
                        else:
                            bandit.attack(knight)
                            sword_sound.play()
                            current_fighter += 1
                            action_cooldown = 0
                else:
                    current_fighter += 1

        #Si todos los luchadores terminaron su turno se resetea al jugador
        if current_fighter > total_fighters:
            current_fighter = 1

    #Revisar si todas las bandidas murieron para aplicar la condicion de game over 1, que es la victoria 
    alive_bandits = 0
    for bandit in bandit_list:
        if bandit.alive == True:
            alive_bandits += 1
    if alive_bandits == 0:
        #Quitar musica poco a poco
        pygame.mixer.music.fadeout(3000)
        game_over = 1

    #Revisar si el juego terminó
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (250, 50))
        if game_over == -1:
            screen.blit(defeat_img, (290, 50))
        if restart_button.draw():
            knight.reset()
            for bandit in bandit_list:
                bandit.reset()
            current_fighter = 1
            action_cooldown
            game_over = 0
            

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()