import pygame,sys
from constantes import*
from auxiliar import*
from pygame.sprite import Group
class Return:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
      
        self.grupo_botones_game_over = Group()
        self.grupo_botones_pause = Group()
       
        self.paused = False
        self.running = True
        self.running_over = True
        self.mostrar_texto = False
        self.game_over = False
        self.reloj = pygame.time.Clock()
        self.imagen_fondo = pygame.image.load(r"C:\Users\Usuario\OneDrive\Escritorio\copia _juego nave\recursos1\espacio.png").convert()
        self.imagen_fondo = pygame.transform.scale(self.imagen_fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
    
    def evento_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        for boton1 in self.grupo_botones_game_over:
            if boton1.rect.collidepoint(mouse_pos) :
                play_soud("sonido\DOORPNUM.WAV",0.2)
                if boton1 == self.boton_menu:
                    from menu import Menu
                    menu = Menu()
                    menu.menu_inicio()
                elif boton1 == self.boton_star:
                    
                    self.running_over = False 
                    # self.running = True
                    # self.game_over = False
                    # print(f"{self.running}   {self.game_over}")
                    # self.ejecutar()
                    from game import Game
                    game = Game()
                    game.ejecutar()
                    # pygame.quit()
                    # sys.exit()
   
    # def control_tiempo(self):
    #     self.tiempo_actual = pygame.time.get_ticks()
    #     self.tiempo_transcurrido = self.tiempo_actual - self.tiempo_inicio
    #     segundos = (self.tiempo_transcurrido // 1000) % 60
    #     dibujar_texto("TIME: {0}".format(segundos),LIMON,self.pantalla,ANCHO_PANTALLA-100,20,20)
    def ejecutar(self):       
      # game over conf
        self.boton_menu = Boton("menu\menu.png",ANCHO_PANTALLA // 2 ,ALTO_PANTALLA // 2 + 40)
        self.boton_star = Boton("menu\star.png",ANCHO_PANTALLA // 2 ,ALTO_PANTALLA // 2 + 100)
        self.tiempo_inicio = pygame.time.get_ticks()
        self.tiempo_nivel = 0

            # print(self.tiempo_nivel)
        while self.running_over:
            # self.flag_control = 
            # print(f"{self.running}{self.game_over}")
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    self.evento_mouse()
            # self.control_pausa_gameover()
            # self.control_tiempo()
            # print(self.tiempo_transcurrido,"     ",self.tiempo_nivel)
            # print(self.tiempo_nivel)
            # if self.enemigo.vida > 0:
            #     self.tiempo_nivel = self.tiempo_transcurrido + 6000

            # if len(self.vida.lista_vidas) > 0:
            #     self.tiempo_nivel = self.tiempo_transcurrido + 6000
            

            # if len(self.vida.lista_vidas) <= 0:
            #     dibujar_texto("FALLED",ORANGE,self.pantalla,ANCHO_PANTALLA//4,ALTO_PANTALLA//4,100)
            #     # self.running = False
            #     self.running = False
            #     # play_soud("recursos1\game_over.ogg",0.5)
            #     if self.tiempo_transcurrido >= self.tiempo_nivel:                
            if self.running_over:
                self.pantalla.blit(self.imagen_fondo, (0, 0))
                dibujar_sprite_estatico("menu\gameover.png",self.pantalla,ANCHO_PANTALLA // 2-200,80,400,200)

                self.grupo_botones_game_over.add(self.boton_menu,self.boton_star)
                self.grupo_botones_game_over.update()
                self.grupo_botones_game_over.draw(self.pantalla)
            # if self.paused:
            #     dibujar_texto("PAUSA",ORANGE,self.pantalla,ANCHO_PANTALLA // 2-150,100,150)
            #     self.grupo_botones_pause.add(self.boton_menu)
            #     self.grupo_botones_pause.update()
            #     self.grupo_botones_pause.draw(self.pantalla)
            # print(len(self.vida.lista_vidas)) 
                # self.grupo_botones_game_over.draw(self.pantalla)
            pygame.display.flip()

            self.reloj.tick(FPS)
        pygame.quit() # Fin
  
# juego = Return ()
# juego.ejecutar()
 