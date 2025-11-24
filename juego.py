#Autor : Santiago Peralta
#Titulo : Ahorcado como temporizador
#Caso de uso : Juego de ahorcado con interfaz gráfica y temporizador usando hilos 


import tkinter as tk
import random
import string
import threading
import time

class Stickman:
    def __init__(self, canvas):
        self.canvas = canvas
        self.parts = []

    def reset(self):
        self.canvas.delete("all")
        self.parts = []

    def draw_next(self):
        index = len(self.parts)
        part = None
        
        if index == 0:
            part = self.canvas.create_line(20, 380, 180, 380, width=4)
        elif index == 1:
            part = self.canvas.create_line(100, 380, 100, 50, width=4)
        elif index == 2:
            part = self.canvas.create_line(100, 50, 200, 50, width=4) 
        elif index == 3:
            part = self.canvas.create_line(200, 50, 200, 100, width=4)
        elif index == 4:
            part = self.canvas.create_oval(170, 100, 230, 160, width=3)
        elif index == 5:
            part = self.canvas.create_line(200, 160, 200, 260, width=4)
        elif index == 6:
            part = self.canvas.create_line(200, 180, 170, 220, width=4)
        elif index == 7:
            part = self.canvas.create_line(200, 180, 230, 220, width=4)
        elif index == 8:
            part = self.canvas.create_line(200, 260, 170, 320, width=4)
        elif index == 9:
            part = self.canvas.create_line(200, 260, 230, 320, width=4)
        
        if part:
            self.parts.append(part)

class Word_bank:
    def __init__(self, words):
        self.words = words
        self.choosen_word = ""
        self.letters_choosen_word = []

    def choose_words(self):
        index = random.randint(0, len(self.words) - 1)
        self.choosen_word = self.words[index]
        self.letters_choosen_word = list(self.choosen_word)
        return self.letters_choosen_word

class Screen:
    def __init__(self, title, size, word_bank):
        self.title = title
        self.size = size
        self.word_bank = word_bank
        self.game_over = False
        self.hints_left = 3
        self.retry = False

        self.screen = tk.Tk()
        self.screen.geometry(self.size)
        self.screen.title(self.title)
        self.screen.resizable(False, False)

        self.top_frame = tk.Frame(self.screen)
        self.top_frame.pack(pady=10, fill="x")

        self.timer_label = tk.Label(self.top_frame, text="Tiempo: 01:00", font=("Arial", 14, "bold"), fg="red")
        self.timer_label.pack(side="left", padx=30)
        
        self.hint_btn = tk.Button(self.top_frame, text=f"Pista ({self.hints_left})", bg="gold", command=self.give_hint)
        self.hint_btn.pack(side="right", padx=30)

        self.label = tk.Label(self.screen, text="", height=1, font=("Arial", 28, "bold"))
        self.label.pack(pady=5) 

        self.canvas = tk.Canvas(self.screen, width=300, height=400, bg="white", highlightthickness=1, highlightbackground="#ccc")
        self.canvas.pack(pady=5)
        self.stickman = Stickman(self.canvas)

        self.frame_buttons = tk.Frame(self.screen)
        self.frame_buttons.pack(pady=15, padx=10)

        self.letters = self.word_bank.choose_words()  
        self.oculta = ["_" for _ in self.letters]   
        self.label.config(text=" ".join(self.oculta))  

        self.create_alphabet_buttons()
        self.start_timer_thread()

    def create_alphabet_buttons(self):
        self.button_map = {}
        for i, letra in enumerate(string.ascii_uppercase):
            boton = tk.Button(
                self.frame_buttons,
                text=letra,
                width=3, 
                height=1,
                font=("Arial", 10, "bold"),
                command=lambda l=letra: self.validator(l)
            )
            boton.grid(row=i // 13, column=i % 13, padx=2, pady=2)
            self.button_map[letra.lower()] = boton

    def give_hint(self):
        if self.hints_left > 0 and not self.game_over:
            indices_ocultos = [i for i, x in enumerate(self.oculta) if x == "_"]
            if not indices_ocultos: return

            idx_random = random.choice(indices_ocultos)
            letra_revelada = self.letters[idx_random]

            for i, l in enumerate(self.letters):
                if l == letra_revelada:
                    self.oculta[i] = letra_revelada
            
            self.label.config(text=" ".join(self.oculta))

            if letra_revelada in self.button_map:
                self.button_map[letra_revelada].config(state="disabled", bg="lightgreen")

            self.hints_left -= 1
            self.hint_btn.config(text=f"Pista ({self.hints_left})")
            
            self.stickman.draw_next()
            
            if len(self.stickman.parts) >= 10:
                self.game_over_action(f"Perdiste. Era: {self.word_bank.choosen_word}")
            
            if "_" not in self.oculta:
                self.game_over = True
                self.timer_label.config(text="¡GANASTE!", fg="green")
                self.label.config(fg="green")
                self.game_over_action("¡GANASTE!")
        
        if self.hints_left == 0:
            self.hint_btn.config(state="disabled")

    def start_timer_thread(self):
        timer_thread = threading.Thread(target=self.timer_worker)
        timer_thread.daemon = True 
        timer_thread.start()

    def timer_worker(self):
        total_seconds = 60
        while total_seconds >= 0 and not self.game_over:
            mins, secs = divmod(total_seconds, 60)
            try:
                self.timer_label.config(text=f"Tiempo: {mins:02}:{secs:02}")
            except: break
            time.sleep(1)
            total_seconds -= 1
        
        if total_seconds == 0:
            self.game_over_action("¡Se acabó el tiempo!")

    def reset_game(self):
        self.retry = True
        self.screen.destroy()

    def game_over_action(self, mensaje):
        self.game_over = True
        self.label.config(text=mensaje, fg="red", font=("Arial", 16, "bold"))
        self.hint_btn.config(state="disabled")
        for btn in self.button_map.values():
            btn.config(state="disabled")
        
        self.btn_reset = tk.Button(self.top_frame, text="Jugar de nuevo", bg="cyan", command=self.reset_game)
        self.btn_reset.pack(side="right", padx=10)

    def validator(self, letra):
        if self.game_over: return 

        letra = letra.lower()
        if letra in self.button_map:
            self.button_map[letra].config(state="disabled")

        if letra in self.letters:
            for i, real in enumerate(self.letters):
                if real == letra:
                    self.oculta[i] = letra
            
            if "_" not in self.oculta:
                self.game_over = True
                self.label.config(text=" ".join(self.oculta), fg="green")
                self.timer_label.config(text="¡GANASTE!", fg="green")
                self.game_over_action("¡GANASTE!")
                return
        else:
            self.stickman.draw_next()
            if len(self.stickman.parts) >= 10:
                self.game_over_action(f"Perdiste. Era: {self.word_bank.choosen_word}") 
                return

        self.label.config(text=" ".join(self.oculta))

    def start(self):
        self.screen.mainloop()

def main():
    palabras = Word_bank(words=["programacion", "teclado", "monitor", "python", "internet", "variable", "funcion"])
    
    while True:
        screen = Screen("Ahorcado", "600x630", palabras)
        screen.start()
        
        if not screen.retry:
            break

if __name__ == "__main__":
    main()

