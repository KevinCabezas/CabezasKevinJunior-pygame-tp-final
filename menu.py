import pygame,sys
from constantes import*
from auxiliar import*
from pygame.sprite import Group
# from game import Game
from pygame import mixer
def reproducir_melodia(ruta):
    pygame.mixer.init()
    pygame.mixer.music.load(ruta)
    pygame.mixer.music.play(-1)  # Reproducir la melodía en bucle infinito
    
def leer_archivo_json():
    with open("datos_juego.json", 'r') as archivo:
        datos = json.load(archivo)
        return datos
def obtener_suma_por_diccionario():
    suma_por_diccionario = []  
    lista = leer_archivo_json()
    for diccionario in lista:
        suma = sum(diccionario.values())
        suma_por_diccionario.append(suma)
    return suma_por_diccionario
def ordenar_lista_mayor_a_menor():
    lista = obtener_suma_por_diccionario()
    lista_ordenada = sorted(lista, reverse=True)
    return lista_ordenada







class Menu():

    def __init__(self) -> None:
        pygame.init()
        mixer.init()
        mixer.music.set_volume(0.5)
        self.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        self.lista_imagenes = []
        self.lista_opciones = []
        self.sprite_fondo = pygame.image.load("recursos\espacio2.png").convert()
        self.sprite_conf = pygame.image.load("recursos\espacio_config.jpg").convert()
        self.sprite_score = pygame.image.load("recursos\espacio_conf.png").convert()
        self.imagen_score = pygame.transform.scale(self.sprite_score,(ANCHO_PANTALLA,ALTO_PANTALLA))
        self.imagen_menu = pygame.transform.scale(self.sprite_fondo,(ANCHO_PANTALLA,ALTO_PANTALLA))
        self.imagen_menu_conf = pygame.transform.scale(self.sprite_conf,(ANCHO_PANTALLA,ALTO_PANTALLA))
        self.menu_principal = True
        self.menu_setting = False
        self.menu_levels = False
        self.menu_score = False
        self.volumen = 0.2
        self.vol = False
        self.grupo_botones = Group()
        self.grupo_botones_conf = Group()
        self.grupo_botones_levels = Group()
        self.grupo_botones_score = Group()
        self.press_cambiar_img  = 0
    def dibujar_score(self):
        lista = ordenar_lista_mayor_a_menor()
        y = 250
        if len(lista) < 10:
            for indice in range(len(lista)):
                texto_formateado = "{0}         {1}".format(str(indice + 1), str(lista[indice]))
                dibujar_texto(texto_formateado,WHITE,self.screen,ANCHO_PANTALLA//2 - 60,y,30)
                y += 35
    def manejar_evento_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.menu_setting:
            for boton in self.grupo_botones_conf:

                if boton.rect.collidepoint(mouse_pos):
                    play_soud("sonido\DOORPNUM.WAV",self.volumen)
                    if boton == self.flecha_baja:
                        if self.press_cambiar_img > 0:
                            print("menos")
                            if self.press_cambiar_img == 0:
                                self.volumen = 0
                            else:
                                self.press_cambiar_img -= 1
                                self.volumen -= 0.5 / 7
                        self.barra_vol = Boton(r"menu\vol_{0}.png".format(self.press_cambiar_img), 205, ALTO_PANTALLA - self.y)
                    elif boton == self.flecha_sube:
                        if self.press_cambiar_img < 6:
                            # if self.pre
                            self.volumen += 0.5/ 7
                            self.press_cambiar_img += 1
                        self.barra_vol = Boton(r"menu\vol_{0}.png".format(self.press_cambiar_img), 205, ALTO_PANTALLA - self.y)
                    elif boton == self.boton_retornar_setting:
                        self.menu_principal = True
                        self.menu_setting = False
        # self.menu_principal
        elif self.menu_principal: 
            for boton in self.grupo_botones:
                if boton.rect.collidepoint(mouse_pos):
                    play_soud("sonido\DOORPNUM.WAV",self.volumen)
                    if boton == self.boton_start:
                        self.menu_principal = False
                        self.menu_setting = False
                        self.vol = True
                        # if menu.menu_principal == False:
                        from game import Game
                        self.game = Game()
                        self.game.ejecutar()
                        pygame.quit()
                        sys.exit()
                    elif boton == self.boton_config:
                        self.menu_setting = True
                        self.menu_principal = False
                    elif boton == self.boton_exit:
                        self.menu_principal = False
                        self.menu_setting = False
                        self.menu_levels = False
                        self.menu_score = False
                    elif boton == self.boton_score:
                        self.menu_score = True
                        self.menu_principal = False
                        self.menu_setting = False
                    elif boton == self.boton_levels:
                        self.menu_levels = True
                        self.menu_score = False
                        self.menu_principal = False
                        self.menu_setting = False
        elif self.menu_levels:
            for boton in self.grupo_botones_levels:
                if boton.rect.collidepoint(mouse_pos):
                    play_soud("sonido\DOORPNUM.WAV",self.volumen)
                    if boton == self.boton_retornar_levels:
                        self.menu_principal = True
                        self.menu_levels = False
        elif self.menu_score:
            for boton in self.grupo_botones_score:
                if boton.rect.collidepoint(mouse_pos):
                    play_soud("sonido\DOORPNUM.WAV",self.volumen)
                    if boton == self.boton_retornar_score:
                        self.menu_principal = True
                        self.menu_score = False
    def menu_inicio(self):
        pygame.font.init()
        screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA)) 
        clock = pygame.time.Clock()

        # pantalla principal config
        self.boton_start = Boton("menu\star.png", ANCHO_PANTALLA // 2- 150, ALTO_PANTALLA // 2 +100)
        self.boton_levels = Boton("menu\levels.png", ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 +100)
        self.boton_exit = Boton("recursos\opcion3.png", ANCHO_PANTALLA // 2+ 150, ALTO_PANTALLA // 2 + 100 )
        self.boton_config = Boton("menu\engrane.png",ANCHO_PANTALLA -103,ALTO_PANTALLA-160,(150,150))
        self.boton_score = Boton("menu\score.png", 915,ALTO_PANTALLA - 2,(130,60))
        self.grupo_botones.add(self.boton_start, self.boton_exit, self.boton_levels,self.boton_config,self.boton_score)
        if self.vol:
            play_soud("recursos1\music.ogg",self.volumen)
      
        # pantalla setting config
        self.y = 150
        self.flecha_sube = Boton("menu\mas.png", 310, ALTO_PANTALLA - self.y)
        self.flecha_baja = Boton("menu\menos.png",  100, ALTO_PANTALLA - self.y)
        self.boton_retornar_setting = Boton(r"menu\back.png", ANCHO_PANTALLA / 2, ALTO_PANTALLA / 2- 80)
        self.grupo_botones_conf.add(self.flecha_sube, self.flecha_baja,self.boton_retornar_setting)
        self.barra_vol = Boton(r"menu\vol_{0}.png".format(self.press_cambiar_img ),  205 , ALTO_PANTALLA - self.y)
        # menu score config
        self.boton_retornar_score = Boton(r"menu\back.png",ANCHO_PANTALLA / 2 , ALTO_PANTALLA  - 100)
        self.grupo_botones_score.add(self.boton_retornar_score)
        # menu levels config
        self.boton_retornar_levels = Boton(r"menu\back.png",ANCHO_PANTALLA / 2, ALTO_PANTALLA - 100)
        self.grupo_botones_levels.add(self.boton_retornar_levels)
        while self.menu_principal or self.menu_setting or self.menu_levels or self.menu_score:
            # print(self.lista_score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.menu_principal:
                        self.menu_principal = False
                        self.menu_score = False
                
                    # else:
                    #     self.menu_levels = False
                    #     # self.menu_setting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.manejar_evento_mouse()                    

            if self.menu_principal:
                screen.blit(self.imagen_menu, (0, 0))
                self.grupo_botones.draw(screen)
                dibujar_texto("SPACE WAR", LIMON, screen, 258, 100, 170)
            elif self.menu_setting:
                self.grupo_botones_conf.add(self.barra_vol)
                screen.blit(self.imagen_menu_conf, (0, 0))
                dibujar_texto("VOLUMEN", MORA, screen, 70, 400, 50)
                dibujar_texto("SETTINGS", ORANGE, screen, 360, 20, 160)
                self.grupo_botones_conf.draw(screen)
            elif self.menu_levels:
                screen.blit(self.imagen_menu_conf, (0, 0))
                dibujar_texto("LEVELS", LIMON, screen, 258, 100, 170)
                self.grupo_botones_levels.draw(screen)
            elif self.menu_score:
                screen.blit(self.imagen_score,(0,0))
                self.dibujar_score()
                dibujar_texto("HIGH SCORE", LIMON, screen, 258, 40, 170)
                self.grupo_botones_score.draw(screen)
            delta_ms = clock.tick(FPS)
            pygame.display.flip()

        pygame.quit() # Fin

menu = Menu()
menu.menu_inicio()

# if menu.menu_principal == False and menu.menu_setting == False:
#         game = Game()
#         game.ejecutar()