import tkinter as tk
import random
import string


class Stickman:
    def __init__(self, canvas):
        self.canvas = canvas
        self.parts = []

    def reset(self):
        self.canvas.delete("all")
        self.parts = []

    def draw_next(self):
        index = len(self.parts)

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

        self.screen = tk.Tk()
        self.screen.geometry(self.size)
        self.screen.title(self.title)

        self.label = tk.Label(self.screen, text="", height=2, font=("Arial", 24))
        self.label.pack(pady=10)

        self.canvas = tk.Canvas(self.screen, width=300, height=400, bg="white")
        self.canvas.pack(pady=20)

        self.stickman = Stickman(self.canvas)

        self.frame_buttons = tk.Frame(self.screen)
        self.frame_buttons.pack(pady=20)

        self.letters = self.word_bank.choose_words()  # palabra elegida
        self.oculta = ["_" for _ in self.letters]      # guiones
        self.label.config(text=" ".join(self.oculta))  # mostrarlos

        self.create_alphabet_buttons()

    def create_alphabet_buttons(self):
        for i, letra in enumerate(string.ascii_uppercase):
            boton = tk.Button(
                self.frame_buttons,
                text=letra,
                width=4,
                height=2,
                command=lambda l=letra: self.validator(l)
            )
            boton.grid(row=i // 9, column=i % 9, padx=5, pady=5)

    def validator(self, letra):
        letra = letra.lower()

        if letra in self.letters:
            for i, real in enumerate(self.letters):
                if real == letra:
                    self.oculta[i] = letra
        else:
            self.stickman.draw_next()

        self.label.config(text=" ".join(self.oculta))

    def start(self):
        self.screen.mainloop()


def main():
    palabras = Word_bank(words=[
        "python", "gato", "perro", "arbol", "ventana", "casa",
        "montana", "juego", "teclado", "raton", "pantalla", "camino",
        "cielo", "nube", "rayo", "tronco", "carro", "barco", "tren",
        "botella", "lapiz", "papel", "libro", "cama", "silla",
        "puerta", "flor", "fuego", "hielo", "lobo", "mono", "robot"
    ])

    screen = Screen("Ahorcado", "800x800", palabras)
    screen.start()


if __name__ == "__main__":
    main()
