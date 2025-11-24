import tkinter as tk #Importa Tkinter
import random #Importa random
import string #Importa coso para generar las letras
import threading #Es la librería para usar nucleos
import time #Es la librería que permite usar el contador

class Stickman: #Es el muñequito
    def __init__(self, canvas): 
        self.canvas = canvas #Los canvas que serían cada una de las lineas
        self.parts = [] #Lista de todas las partes ya dibujadas

    def reset(self): #Es el metodo que borra el muñequito
        self.canvas.delete("all")
        self.parts = [] #Lista de todas las partes ya dibujadas

    def draw_next(self): #Es el metodo que hace que las partes se dibujen en orden
        index = len(self.parts) #Esto cuenta las partes que ya se dibujaron y en base a eso elige dibujar la siguiente
        part = None 
        # Coordenadas ajustadas al canvas de 400px de alto
        if index == 0:
            part = self.canvas.create_line(20, 380, 180, 380, width=4) # Piso
        elif index == 1:
            part = self.canvas.create_line(100, 380, 100, 50, width=4) # Poste
        elif index == 2:
            part = self.canvas.create_line(100, 50, 200, 50, width=4)  # Techo
        elif index == 3:
            part = self.canvas.create_line(200, 50, 200, 100, width=4) # Cuerda
        elif index == 4:
            part = self.canvas.create_oval(170, 100, 230, 160, width=3) # Cabeza
        elif index == 5:
            part = self.canvas.create_line(200, 160, 200, 260, width=4) # Cuerpo
        elif index == 6:
            part = self.canvas.create_line(200, 180, 170, 220, width=4) # Brazo I
        elif index == 7:
            part = self.canvas.create_line(200, 180, 230, 220, width=4) # Brazo D
        elif index == 8:
            part = self.canvas.create_line(200, 260, 170, 320, width=4) # Pierna I
        elif index == 9:
            part = self.canvas.create_line(200, 260, 230, 320, width=4) # Pierna D
        
        if part: # Añade las partes a la lista de partes
            self.parts.append(part)

class Word_bank:
    def __init__(self, words):
        self.words = words #Recibe del main las palabras
        self.choosen_word = "" #Esta es la palabra que se elige al azar
        self.letters_choosen_word = [] #Acá van las letras separadas de la palabra al azar

    def choose_words(self): #Este metodo es el que elige la palabra al azar
        index = random.randint(0, len(self.words) - 1) #Esta linea escoge un indice al azar en funcion de cuantas palabras hayan
        self.choosen_word = self.words[index] #Selecciona la palabra de la lista por el indice
        self.letters_choosen_word = list(self.choosen_word) #Esto con List separa cada letra
        return self.letters_choosen_word # y retorna la lista de caracteres

class Screen: #Aca es la pantalla
    def __init__(self, title, size, word_bank): #la pantalla recibe la clase del banco de palabras y del main titulo y tamaño 
        self.title = title
        self.size = size
        self.word_bank = word_bank #Esta es la clase word_bank
        self.game_over = False #Si perdió el juego
        self.hints_left = 3 #Las pistas que tiene
        self.retry = False #Si el jugador quiere jugar de nuevo es true

        self.screen = tk.Tk() #Define la pantalla
        self.screen.geometry(self.size) #Define el tamaño
        self.screen.title(self.title) #Define el titulo
        self.screen.resizable(False, False) # Bloquear el redimensionamiento para que quede pequeño y no se salgan los botones

        self.top_frame = tk.Frame(self.screen) #Crea un frame
        self.top_frame.pack(pady=10, fill="x") # pady reducido

        #La etiqueta donde se muestra el tiempo que queda
        self.timer_label = tk.Label(self.top_frame, text="Tiempo: 01:00", font=("Arial", 14, "bold"), fg="red")
        #Acá mete la etiqueta en el frame
        self.timer_label.pack(side="left", padx=30)
        #El boton para tener la pista, este llama a la funcion obtener pista
        self.hint_btn = tk.Button(self.top_frame, text=f"Pista ({self.hints_left})", bg="gold", command=self.give_hint)
        #Acá mete el boton al frame
        self.hint_btn.pack(side="right", padx=30)

        #Acá es donde va la palabra que se tiene que adivinar
        self.label = tk.Label(self.screen, text="", height=1, font=("Arial", 28, "bold"))
        self.label.pack(pady=5) 

        #Acá es donde dibuja los canvas
        self.canvas = tk.Canvas(self.screen, width=300, height=400, bg="white", highlightthickness=1, highlightbackground="#ccc")
        self.canvas.pack(pady=5)
        self.stickman = Stickman(self.canvas)

        #Teclado
        self.frame_buttons = tk.Frame(self.screen)
        self.frame_buttons.pack(pady=15, padx=10)

        self.letters = self.word_bank.choose_words() #Saca las letras de la palabra elegida  
        self.oculta = ["_" for _ in self.letters] #Oculta las letras reemplazandolas por guiones   
        self.label.config(text=" ".join(self.oculta)) #Esto mete los guines a la etiqueta de mas arriba  

        self.create_alphabet_buttons() #Crea los botones
        self.start_timer_thread() #Crea el hilo que tiene el contador

    def create_alphabet_buttons(self):
        self.button_map = {} #Hace un diccionario con nombre: Letra valor: boton creado
        for i, letra in enumerate(string.ascii_uppercase): #string.ascii_uppercase Esto es una lista de todas las minusculas
            boton = tk.Button(
                self.frame_buttons,#Los introduce en el frame de botones
                text=letra, #Les escribe cada letra
                width=3, 
                height=1,
                font=("Arial", 10, "bold"),
                command=lambda l=letra: self.validator(l) #Cada vez que se presiona un boton llama esta funcion de validar
            )
            boton.grid(row=i // 13, column=i % 13, padx=2, pady=2) #Esto acomoda los botones
            self.button_map[letra.lower()] = boton #Mete cada boton en el diccionario con su respectiva letra como nombre

    def give_hint(self): #Metodo que da una pista
        if self.hints_left > 0 and not self.game_over: #Esto valida que aun queden pistas y el jugador no haya perdido
            indices_ocultos = [i for i, x in enumerate(self.oculta) if x == "_"] #Revisa si hay guines que revelar
            if not indices_ocultos: return #Para si no encuentra guiones que revelar

            idx_random = random.choice(indices_ocultos) #Elige un guion random de los que haya encontrado
            letra_revelada = self.letters[idx_random] #Le asigna el nombre de letra revelada a la que eligio

            for i, l in enumerate(self.letters):
                if l == letra_revelada: #Busca la letra que eligio en self.letters 
                    self.oculta[i] = letra_revelada #Cambia el guion por la letra correspondiente
            
            self.label.config(text=" ".join(self.oculta)) #Cambia la etiqueta de guiones con la nueva información

            if letra_revelada in self.button_map: #El boton que se pulsó con la pista se tiñe de verde y se deshabilita
                self.button_map[letra_revelada].config(state="disabled", bg="lightgreen")

            self.hints_left -= 1 #Le quita una pista a las pistas actuales del comienzo
            self.hint_btn.config(text=f"Pista ({self.hints_left})") #Actualiza la información del botón
            
            self.stickman.draw_next() #Dibuja una parte del muñeco cuando pide una pista
            
            if len(self.stickman.parts) >= 10:
                self.game_over_action(f"Perdiste. Era: {self.word_bank.choosen_word}")
            
            if "_" not in self.oculta: #Si ya no hay guiones el juego se acaba y el jugador gana
                self.game_over = True
                self.timer_label.config(text="¡GANASTE!", fg="green") #Gana
                self.label.config(fg="green")
        
        if self.hints_left == 0: #Si no quedan pistas disponibles se desactiva el boton
            self.hint_btn.config(state="disabled")

    def start_timer_thread(self): #Crea el hilo que se va a encargar del temporizador
        timer_thread = threading.Thread(target=self.timer_worker) #Aca se pone la funcion que va a estar en "segundo plano"
        timer_thread.daemon = True 
        timer_thread.start() #Crea el nuevo hilo

    def timer_worker(self): #Metodo que hace funcionar el contador
        total_seconds = 60 # 1 Minuto 
        while total_seconds >= 0 and not self.game_over: #Mientras hayan segundos y no se haya acabado el juego -->
            mins, secs = divmod(total_seconds, 60) #Esto pasa los segundos a minutos con segundos, es necesario si se quiere dar mas que 1 min, antes eran 10 y era necesario
            try: #Intenta actualizar la etiqueta
                self.timer_label.config(text=f"Tiempo: {mins:02}:{secs:02}")
            except: break #Si falla termina el hilo
            time.sleep(1) #Establece el tiempo en que cambia en un segundo, espera un segundo hasta ejecutarse de vuelta
            total_seconds -= 1 #va restando un segundo cada segundo
        
        if total_seconds == 0: #Si ya no hay segundos el jugador pierde por tiempo
            self.game_over_action("¡Se acabó el tiempo!")

    
    def reset_game(self): #Reinicia el juego
        self.retry = True # Le dice al main que si quiere reiniciar
        self.screen.destroy() # Destruye la ventana actual para que el main cree otra

    def game_over_action(self, mensaje):
        self.game_over = True #Acaba el juego
        self.label.config(text=mensaje, fg="red", font=("Arial", 16, "bold")) #Acá pone que perdió en rojo y recibe la causa
        self.hint_btn.config(state="disabled") #Deshabilita el boton de pistas
        for btn in self.button_map.values():
            btn.config(state="disabled") #Deshabilita los botones del teclado
        
        #Muestra el boton de reiniciar cuando acaba el juego
        self.btn_reset = tk.Button(self.top_frame, text="Jugar de nuevo", bg="cyan", command=self.reset_game)
        self.btn_reset.pack(side="right", padx=10)

    def validator(self, letra): #Valida cada letra presionada
        if self.game_over: return #Si el jugador ya perdió este proceso no va

        letra = letra.lower() #Cambia a minuscula por si acaso
        if letra in self.button_map: #Deshabilita la tecla presionada
            self.button_map[letra].config(state="disabled")

        if letra in self.letters:
            for i, real in enumerate(self.letters): #Si letra está en la lista de letras de la palabra la revela
                if real == letra:
                    self.oculta[i] = letra
            
            if "_" not in self.oculta: #Si no hay guiones que revelar acaba el juego
                self.game_over = True
                self.label.config(text=" ".join(self.oculta), fg="green")
                self.timer_label.config(text="¡GANASTE!", fg="green") #Ganaste :v
                
                # ### NUEVO: Si gana, tambien mostramos el boton ###
                self.game_over_action("¡GANASTE!") # Llamamos a game_over_action para deshabilitar todo y mostrar el boton
                return
        else:
            self.stickman.draw_next() #Si la letra no está en las letras de la palabra entonces dibuja el muñequito
            if len(self.stickman.parts) >= 10: #Primero revisa si hacen falta partes que dibujar
                #Si ya no queda que dibujar el jugador pierde
                self.game_over_action(f"Perdiste. Era: {self.word_bank.choosen_word}") 
                return

        self.label.config(text=" ".join(self.oculta)) #Actualiza la información de la etiqueta

    def start(self): #Metodo que inicia el mainloop de la ventana
        self.screen.mainloop()

def main():
    palabras = Word_bank(words=["programacion", "teclado", "monitor", "python", "internet", "variable", "funcion"])
    #Crea el banco de palabras
    
    while True:
        screen = Screen("Ahorcado", "600x630", palabras)
        #Crea la pantalla
        screen.start() #Inicia la ventana
        
        #Si el usuario cerró la ventana con la X, screen.retry es False y el bucle se rompe (se cierra el programa)
        #Si el usuario dio click a "Jugar de nuevo", screen.retry es True y el bucle sigue (crea nueva ventana)
        if not screen.retry:
            break

if __name__ == "__main__":
    main() #Ejecuta el main