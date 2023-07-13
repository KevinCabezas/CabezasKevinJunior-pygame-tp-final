import pygame,sys
from constantes import*
from trampas import Meteoro
# from trampa2 import Asteroide
from explocion import Explosion
from vida import Vida
from player import Player
from items import Item
from enemigo import Enemigo,Enemigo_dos
from balas import Bullet
from item_bala import Item_doble
from item_fuego import Item_fuego
from auxiliar import*
from pygame.sprite import Group
from retorno import Return

class NivelTres:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        self.sonido_disparo = None
        self.grupo_sprites = Group()
        self.grupo_meteoros = Group()
        self.grupo_asteroide = Group()
        self.grupo_bullets = Group()
        self.grupo_items_vida = Group()
        self.grupo_items_doble = Group()
        self.grupo_items_fuego = Group()
        self.grupo_blas_enemigo = Group()
        self.grupo_botones_game_over = Group()
        self.grupo_botones_pause = Group()
        self.grupo_enemigos = Group()
        self.vida = Vida()
        self.choco = False
        self.vida.vida_player()
        self.cambiar_bala_doble = False
        self.cambiar_bala_fuego = False
        self.cambiar_bala_simple = True
        self.paused = False
        self.running = True
        self.running_over = True
        self.mostrar_texto = False
        self.game_over = False
        self.escudo = 100
        self.tiempo_inicial = 0
        self.tiempo_inicio = 0
        self.tiempo_mostrando_texto = 600 
        self.tiempo_transcurrido = 0
        self.score_general = 0
        self.datos_score = []
        self.reloj = pygame.time.Clock()
        self.imagen_fondo = pygame.image.load(r"recursos\espacio_conf.png").convert()
        self.imagen_fondo = pygame.transform.scale(self.imagen_fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.generar_sprites()
        self.texto = "¡Astronauta valiente!\n" \
        "Tu objetivo es vencer al enemigo final y asegurar la victoria absoluta.\n" \
        "Esta batalla será épica y determinará el destino de la galaxia.\n" \
        "¡Derrota a ese enemigo despiadado y reclama la gloria!\n" \
        "¡Buena suerte, astronauta, el destino de la galaxia está en tus manos!"

    def generar_sprites(self):
        self.player = Player(self.grupo_sprites,self.grupo_bullets)
        self.enemigo = Enemigo(self.grupo_sprites,self.grupo_blas_enemigo,"recursos\enemigo_sup.png",r"recursos\fuego_p.png",180,180,200)
        # grupo_enemigos = pygame.sprite.Group()
        self.enemigo1 = Enemigo_dos(self.grupo_sprites,self.grupo_blas_enemigo,1,-150,200)
        self.enemigo2 = Enemigo_dos(self.grupo_sprites,self.grupo_blas_enemigo,2,-150,200)
        self.enemigo3 = Enemigo_dos(self.grupo_sprites,self.grupo_blas_enemigo,3,ANCHO_PANTALLA + 150,200)
        self.enemigo4 = Enemigo_dos(self.grupo_sprites,self.grupo_blas_enemigo,4,ANCHO_PANTALLA + 150,200)
        self.enemigo5 = Enemigo_dos(self.grupo_sprites,self.grupo_blas_enemigo,1,-150,100)
        self.enemigo6 = Enemigo_dos(self.grupo_sprites,self.grupo_blas_enemigo,2,-150,100)
        self.enemigo7 = Enemigo_dos(self.grupo_sprites,self.grupo_blas_enemigo,3,ANCHO_PANTALLA + 150,100)
        self.enemigo8 = Enemigo_dos(self.grupo_sprites,self.grupo_blas_enemigo,4,ANCHO_PANTALLA + 150,100)


        # self.grupo_sprites.add(self.enemigo1)
        self.grupo_sprites.add(self.enemigo1,self.enemigo2,self.enemigo3,self.enemigo4,self.enemigo5,self.enemigo6,self.enemigo7,self.enemigo8)
        self.grupo_enemigos.add(self.enemigo1,self.enemigo2,self.enemigo3,self.enemigo4,self.enemigo5,self.enemigo6,self.enemigo7,self.enemigo8)
        self.grupo_sprites.add(self.player)
    
        for i in range(5):
            asteriode = Meteoro()
            self.grupo_sprites.add(asteriode) 
            self.grupo_asteroide.add(asteriode)
        for i in range(1):
            item = Item()
            self.grupo_sprites.add(item) 
            self.grupo_items_vida.add(item)
        for i in range(1):
            item_doble_bala = Item_doble()
            self.grupo_sprites.add(item_doble_bala) 
            self.grupo_items_doble.add(item_doble_bala)
        # for i in range(1):
        #     item_fuego = Item_fuego()
        #     self.grupo_sprites.add(item_fuego)
        #     self.grupo_items_fuego.add(item_fuego)

   
    def play_soud(self,ruta):
        self.sonido_disparo = pygame.mixer.Sound(ruta)
        self.sonido_disparo.play()
        self.volumen = VOLUMEN
        self.sonido_disparo.set_volume(self.volumen)
  

    def leer_archivo_json(self,ruta):
        with open(ruta, 'r') as archivo:
            datos = json.load(archivo)
            return datos
    def guardar_datos(self):
        with open("score3.json", 'w') as archivo:
            json.dump(self.score_general, archivo)


    def colicion_item_vida_player(self):
        choques = pygame.sprite.spritecollide(self.player,self.grupo_items_vida,True)
        for choque in choques:
            item_vida = Item()
            self.grupo_sprites.add(item_vida)
            self.grupo_items_vida.add(item_vida)   
            self.vida.aumentar_vida(True)
            self.play_soud("sonido\BLIP.WAV")
        self.vida.dibujar_vidas(self.pantalla,"nada")

    def choque_item_doble_player(self):
        choco = False
        choques = pygame.sprite.spritecollide(self.player,self.grupo_items_doble,True)
        for choque in choques:
            item_doble_bala = Item_doble()
            self.grupo_sprites.add(item_doble_bala)
            self.grupo_items_doble.add(item_doble_bala)
            self.cambiar_bala_doble = True
            self.cambiar_bala_fuego = False
            self.cambiar_bala_simple = False
            self.choco = True

    def choque_item_fuego_player(self):
        choques = pygame.sprite.spritecollide(self.player,self.grupo_items_fuego,True)
        for choque in choques:
            item_fuego = Item_fuego()
            self.grupo_sprites.add(item_fuego)
            self.grupo_items_fuego.add(item_fuego)
            self.cambiar_bala_fuego = True
            self.cambiar_bala_simple = False
            self.cambiar_bala_doble = False

     #colicion balas con asteriodes
    def colision_balas_asteroides(self):
        hits = pygame.sprite.groupcollide(self.grupo_asteroide, self.grupo_bullets, True, True)
        for hit in hits:
            self.play_soud("sonido\BANGLRG.WAV")
            explocion = Explosion(hit.rect.center)
            self.grupo_sprites.add(explocion)

            asteriode = Meteoro()
            self.grupo_sprites.add(asteriode)
            self.grupo_asteroide.add(asteriode) 
            self.score_general += 15
  #colicion jugador con asteriode
    def colision_jugador_asteroide(self):
        hits = pygame.sprite.spritecollide(self.player, self.grupo_asteroide, True)
        for hit in hits:
            explocion = Explosion(hit.rect.center)
            self.grupo_sprites.add(explocion)
            asteriode = Meteoro()
            self.grupo_sprites.add(asteriode)
            self.grupo_asteroide.add(asteriode)
            self.escudo -= 5
            if self.escudo <= 0:
                self.vida.eliminar_vidas(True)
    # def control_pausa_gameover(self):
    #     if len(self.vida.lista_vidas) == 0:
    #         self.game_over = True
    #         self.running = False
            

    # colision laser item
    def colision_laser_item(self):
        hits = pygame.sprite.groupcollide(self.grupo_items_vida, self.grupo_bullets, True, True)
        for hit in hits:
            item = Item()
            self.grupo_sprites.add(item)
            self.grupo_items_vida.add(item)
            self.vida.eliminar_vidas(True)
            self.tiempo_inicial = pygame.time.get_ticks()
            if self.enemigo.vida > 0:
                self.enemigo.vida += 10
                self.mostrar_texto = True   
        if self.mostrar_texto and pygame.time.get_ticks() - self.tiempo_inicial <= self.tiempo_mostrando_texto:   
            font = pygame.font.Font(None, 30)
            text = font.render("live enemi +10...", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.pantalla.get_width() // 2, self.pantalla.get_height() // 2))
            self.pantalla.blit(text, text_rect)
        else:   
            self.mostrar_texto = False

    def colision_laser_enemigo_dos(self):
        for enemigo in self.grupo_enemigos:
            impactos = pygame.sprite.spritecollide(enemigo,self.grupo_bullets,True)
            for impacto in impactos:
                self.play_soud("sonido\BANGHUGE.WAV")
                if enemigo == self.enemigo1:  
                    self.enemigo1.vida -= 5
                elif enemigo == self.enemigo2:
                    self.enemigo2.vida -= 5
                elif enemigo == self.enemigo3:
                    self.enemigo3.vida -= 5
                elif enemigo == self.enemigo4:
                    self.enemigo4.vida -= 5
                elif enemigo == self.enemigo5:  
                    self.enemigo5.vida -= 5
                elif enemigo == self.enemigo6:
                    self.enemigo6.vida -= 5
                elif enemigo == self.enemigo7:
                    self.enemigo7.vida -= 5
                elif enemigo == self.enemigo8:
                    self.enemigo8.vida -= 5    
                if self.cambiar_bala_doble:
                    punto_explocion = (impacto.rect.center[0],impacto.rect.center[1]-20)
                if self.cambiar_bala_simple:
                    punto_explocion = (impacto.rect.center[0],impacto.rect.center[1]-20) 
                if self.cambiar_bala_fuego:
                    punto_explocion = (impacto.rect.center[0],impacto.rect.center[1]-100)
                explocion = Explosion(punto_explocion)
                self.grupo_sprites.add(explocion)
                self.score_general += 20
        
    # colicion laserjugador con enemigo
    def colision_laser_enemigo(self):
        daños = pygame.sprite.spritecollide(self.enemigo,self.grupo_bullets,True)
        for daño in daños:
            self.play_soud("sonido\BANGHUGE.WAV")
            self.enemigo.vida -= 10
            if self.cambiar_bala_doble:
                punto_explocion = (daño.rect.center[0],daño.rect.center[1]-20)
            if self.cambiar_bala_simple:
                punto_explocion = (daño.rect.center[0],daño.rect.center[1]-20) 
            if self.cambiar_bala_fuego:
                punto_explocion = (daño.rect.center[0],daño.rect.center[1]-100)
            explocion = Explosion(punto_explocion)
            self.grupo_sprites.add(explocion)
            self.score_general += 20
    def colision_laser_player(self):
        impactos = pygame.sprite.spritecollide(self.player,self.grupo_blas_enemigo,True)
        for impacto in impactos:
            self.play_soud("sonido\BANGLRG.WAV")
            explocion = Explosion(impacto.rect.center)
            self.grupo_sprites.add(explocion)
            self.escudo -= 10
            if self.escudo <= 0:
                self.vida.eliminar_vidas(True)

    def puntuacion_draw(self):
        dibujar_texto("SCORE",LIMON,self.pantalla,ANCHO_PANTALLA-100,70,25)
        dibujar_texto(str(self.score_general),ORANGE,self.pantalla,ANCHO_PANTALLA-100,110,20)
        dibujar_texto(str(len(self.vida.lista_vidas)),ORANGE,self.pantalla,ANCHO_PANTALLA-100,130,20)

    def dibujar_parrafo(self):
        # Dividir el texto en líneas
        lines = self.texto.splitlines()

        # Posición inicial del texto
        x = 200
        y = 210
        for line in lines:
            dibujar_texto(line,WHITE,self.pantalla,x,y,30)
            y += 40
    def evento_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.game_over :
            for boton1 in self.grupo_botones_game_over:
                if boton1.rect.collidepoint(mouse_pos) :
                    play_soud("sonido\DOORPNUM.WAV",self.volumen)
                    if boton1 == self.boton_menu:
                        print("menu")
                        pass
                    elif boton1 == self.boton_star:
                        
                        # self.running_over = False 
                        self.running = True
                        # self.game_over = False
                        print(f"{self.running}   {self.game_over}")
                        self.ejecutar()


                        # self.game_over = False
                        pass
        elif self.paused:
            for boton in self.grupo_botones_pause:
                if boton.rect.collidepoint(mouse_pos) :
                    play_soud("sonido\DOORPNUM.WAV",0.2)
                    if boton == self.boton_menu:
                        pass
    def escudo_player(self):
        ancho_barra = 100
        alto_barra = 17
        x = 10
        y = 80
        fill = (self.escudo / 100) * ancho_barra
        border = pygame.Rect(x, y, ancho_barra, alto_barra)
        fill = pygame.Rect(x, y, fill, alto_barra)
        pygame.draw.rect(self.pantalla, LIMON, fill)
        pygame.draw.rect(self.pantalla, WHITE, border, 2)
        dibujar_texto("SHIELD",ORANGE,self.pantalla,10,50,20)
    def control_tiempo(self):
        self.tiempo_actual = pygame.time.get_ticks()
        self.tiempo_transcurrido = self.tiempo_actual - self.tiempo_inicio
        segundos = (self.tiempo_transcurrido // 1000) % 60
        dibujar_texto("TIME: {0}".format(segundos),LIMON,self.pantalla,ANCHO_PANTALLA-100,20,20)
    def ejecutar(self):       
      # game over conf
        self.boton_menu = Boton("menu\menu.png",ANCHO_PANTALLA // 2 ,ALTO_PANTALLA // 2 + 40)
        self.boton_star = Boton("menu\star.png",ANCHO_PANTALLA // 2 ,ALTO_PANTALLA // 2 + 100)
        self.tiempo_inicio = pygame.time.get_ticks()
        self.tiempo_game_over = 0
        self.tiempo_mision_ok = 0

        #     print(self.tiempo_nivel)
        while self.running_over:
            print("nivel 1")
            # self.flag_control = 
            # print(f"{self.running}{self.game_over}")
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    # self.guradar_datos_game()  
                    # print(self.game_over)
                    # self.datos.append(self.score)
                    # self.running = False
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:    
                        if self.cambiar_bala_doble:
                            self.player.double_shoot()
                        if self.cambiar_bala_simple:
                            self.player.shoot() 
                        if self.cambiar_bala_fuego:
                            self.player.shoot_fire_bol()
                        self.play_soud("sonido\RIFLE.WAV")
                    if evento.key == pygame.K_RETURN:
                        self.paused = not self.paused
                    if evento.key == pygame.K_ESCAPE:
                        # self.running = False
                        # pygame.quit()
                        # sys.exit()
                        self.cambiar_nivel()
                        print("ok")
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    self.evento_mouse()
            # self.control_pausa_gameover()
            self.control_tiempo()
            # print(self.tiempo_transcurrido,"     ",self.tiempo_game_over)
            # print(self.tiempo_nivel)
            if self.enemigo.vida > 0:
                self.tiempo_mision_ok = self.tiempo_transcurrido + 6000

            if len(self.vida.lista_vidas) > 0:
                self.tiempo_game_over = self.tiempo_transcurrido + 6000
            

            # if not self.paused :
            if  self.running:
                if self.tiempo_transcurrido > 0:
                    self.pantalla.blit(self.imagen_fondo, (0, 0))
                    dibujar_texto("MISSION 3",ORANGE,self.pantalla,ANCHO_PANTALLA//3,20,130)
                    self.dibujar_parrafo()

                if self.tiempo_transcurrido > 6000:
                    self.pantalla.blit(self.imagen_fondo, (0, 0))
                    self.grupo_sprites.update()
                    self.grupo_sprites.draw(self.pantalla)
                if self.enemigo1.vida == 0:
                # if (self.enemigo1.vida == 0 and  self.enemigo2.vida == 0 and self.enemigo3.vida == 0 and self.enemigo4.vida == 0 and
                #     self.enemigo5.vida == 0 and  self.enemigo6.vida == 0 and self.enemigo7.vida == 0 and self.enemigo8.vida == 0):
                    self.grupo_sprites.add(self.enemigo)
                if self.enemigo.vida <= 0:
                    # self.guardar_datos()
                    self.guardar = GuardarDatos(self.leer_archivo_json("score1.json"),self.leer_archivo_json("score2.json"),self.score_general)
                    dibujar_texto("MISSION COMPLET",ORANGE,self.pantalla,ANCHO_PANTALLA//4,ALTO_PANTALLA//3,100)
                    if self.tiempo_transcurrido >= self.tiempo_mision_ok:                
                        self.running = False
                        retorno = Return()
                        retorno.ejecutar()
                        pygame.quit()
                        sys.exit()
                # if self.tiempo_transcurrido > 21000:
                #     # self.running_over = False
                self.control_tiempo()
                # colision items con player
            if self.tiempo_transcurrido > 8000:  
                self.colicion_item_vida_player() 
                self.choque_item_doble_player()
                self.choque_item_fuego_player()
                if self.choco:
                    self.vida.dibujar_vidas(self.pantalla,"D")
                # colision 
                self.colision_balas_asteroides()
                self.colision_laser_enemigo()
                self.colision_laser_enemigo_dos()
                self.colision_laser_item()
                self.colision_laser_player()
                # score 
                self.puntuacion_draw()
                self.escudo_player()
                self.colision_jugador_asteroide() 
            if len(self.vida.lista_vidas) <= 0:
                self.guardar = GuardarDatos(self.leer_archivo_json("score1.json"),self.leer_archivo_json("score2.json"),self.score_general)
                # guardar.guardar_datos_juego() 
                dibujar_texto("FALLED",ORANGE,self.pantalla,ANCHO_PANTALLA//4,ALTO_PANTALLA//4,100)
                # self.running = False
                self.running = False
                retorno = Return()
                retorno.ejecutar()
            if self.paused:
                dibujar_texto("PAUSA",ORANGE,self.pantalla,ANCHO_PANTALLA // 2-150,100,150)
                self.grupo_botones_pause.add(self.boton_menu)
                self.grupo_botones_pause.update()
                self.grupo_botones_pause.draw(self.pantalla)
            # print(len(self.vida.lista_vidas)) 
                # self.grupo_botones_game_over.draw(self.pantalla)
            pygame.display.flip()

            self.reloj.tick(FPS)
        pygame.quit() # Fin
   
# juego = NivelTres ()
# juego.ejecutar()
 