# Juego del Ahorcado en Python
Un clásico juego del Ahorcado desarrollado con Python y la librería gráfica Tkinter. Este proyecto va más allá de la implementación básica, integrando hilos (threading) para gestionar un temporizador en tiempo real y un sistema de pistas con penalización.

## Características:
Interfaz Gráfica (GUI): Interfaz limpia y compacta creada con Tkinter.

## Temporizador en Tiempo Real: 
Cuenta regresiva de 60 segundos implementada con threading para no congelar la interfaz del juego.

## Sistema de Pistas:

El jugador tiene 3 pistas disponibles.

Costo: Pedir una pista revela una letra al azar, pero dibuja una parte del muñeco (penalización).

Visualización en el teclado virtual (las teclas regaladas se marcan en verde).

Reinicio Rápido: Opción para "Jugar de nuevo" sin cerrar la ventana al finalizar la partida.

## Programación Orientada a Objetos (POO): 
Código organizado en clases (Stickman, Word_bank, Screen) para mayor escalabilidad.

## Requisitos
Para ejecutar este juego necesitas tener instalado Python 3.x. El juego utiliza solo librerías estándar de Python, por lo que no necesitas instalar nada extra con pip.

Librerías utilizadas:

- tkinter (Interfaz gráfica)

- threading (Concurrencia)

- time (Manejo del tiempo)

- random (Selección aleatoria)

- string (Manejo del alfabeto)

## Instalación y Ejecución
1. Clona este repositorio o descarga el archivo .py.

2. Abre tu terminal o línea de comandos.

3. Navega hasta la carpeta donde guardaste el archivo.

4. Ejecuta el siguiente comando:

### Bash

python nombre_de_tu_archivo.py
### Cómo Jugar
<img width="601" height="671" alt="image" src="https://github.com/user-attachments/assets/e1a4badf-3642-4faf-9e84-5bde17812957" />

Objetivo: Adivinar la palabra oculta antes de que se dibuje el muñeco completo o se acabe el tiempo.

Tiempo: Tienes exactamente 1 minuto.

Intentos: Puedes cometer hasta 10 errores antes de perder.

Pistas:

Presiona el botón "Pista" si estás atascado.

¡Cuidado! Usar una pista cuenta como un error y dibujará una parte del muñeco.

Ganar/Perder:

Ganas si completas la palabra.

Pierdes si el muñeco se completa o el reloj llega a 00:00.

## Estructura del Código
El código está dividido en clases para mantener el orden:

Stickman: Controla el dibujo del muñeco en el Canvas.

Word_bank: Gestiona la lista de palabras y la selección aleatoria.

Screen: Clase principal que maneja la ventana, los widgets, los hilos y la lógica del juego.

main: Punto de entrada y bucle de reinicio del juego.

## Autor
Desarrollado como práctica de conceptos avanzados de Python (Threading y GUI). Santiago Peralta
