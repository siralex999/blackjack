import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

# Conteo Hi-Lo por valor
conteo_hi_lo = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

niveles = {
    "Fácil": 2000,
    "Medio": 1000,
    "Difícil": 500
}

valores = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
palos = ['clubs', 'diamonds', 'hearts', 'spades']
opciones = list(niveles.keys())

# Mapeo para nombres de archivos
nombre_archivo = {
    'A': 'ace',
    'J': 'jack',
    'Q': 'queen',
    'K': 'king',
    '10': '10',
    '9': '9',
    '8': '8',
    '7': '7',
    '6': '6',
    '5': '5',
    '4': '4',
    '3': '3',
    '2': '2'
}


class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Conteo de Blackjack")
        self.root.geometry("500x400")
        self.root.configure(bg="darkgreen")

        self.seleccion_actual = 0
        self.carta_img = None

        self.crear_pantalla_inicio()
        self.root.bind("<Up>", self.mover_arriba)
        self.root.bind("<Down>", self.mover_abajo)

    def crear_baraja(self):
        baraja = [(valor, palo) for valor in valores for palo in palos]
        random.shuffle(baraja)
        print(f"Baraja creada y mezclada. Total cartas: {len(baraja)}")
        return baraja

    def crear_pantalla_inicio(self):
        self.limpiar_pantalla()

        tk.Label(self.root, text="Selecciona nivel de dificultad:",
                 font=("Arial", 16), fg="white", bg="darkgreen").pack(pady=20)

        self.botones = []
        for i, nivel in enumerate(opciones):
            b = tk.Button(self.root, text=nivel, font=("Arial", 14), width=15,
                         bg="white", command=lambda n=nivel: self.iniciar_juego(n))
            b.pack(pady=5)
            self.botones.append(b)

        self.actualizar_cursor()

        # ✅ Activar Enter para seleccionar dificultad
        self.root.bind("<Return>", self.seleccionar_opcion)

    def actualizar_cursor(self):
        for i, b in enumerate(self.botones):
            if i == self.seleccion_actual:
                b.config(bg="lightblue")
            else:
                b.config(bg="white")

    def mover_arriba(self, event):
        self.seleccion_actual = (self.seleccion_actual - 1) % len(self.botones)
        self.actualizar_cursor()

    def mover_abajo(self, event):
        self.seleccion_actual = (self.seleccion_actual + 1) % len(self.botones)
        self.actualizar_cursor()

    def seleccionar_opcion(self, event=None):
        self.botones[self.seleccion_actual].invoke()

    def iniciar_juego(self, nivel):
        print(f"Nivel elegido: {nivel}")
        self.tiempo = niveles.get(nivel, 1000)
        print(f"Tiempo entre cartas (ms): {self.tiempo}")

        baraja_completa = self.crear_baraja()

        # Seleccionamos aleatoriamente entre 20 y 50 cartas para mostrar
        cantidad_cartas = random.randint(20, 50)
        print(f"Mostrando {cantidad_cartas} cartas de la baraja")

        self.baraja = baraja_completa[:cantidad_cartas]

        self.index = 0
        self.cuenta_real = 0
        self.limpiar_pantalla()

        self.label_img = tk.Label(self.root, bg="darkgreen")
        self.label_img.pack(pady=40)

        self.root.after(1000, self.mostrar_siguiente_carta)

    def construir_nombre_archivo(self, valor, palo):
        nombre_valor = nombre_archivo[valor]
        # Las figuras terminan en "2"
        if valor in ['J', 'Q', 'K']:
            return f"{nombre_valor}_of_{palo}2.png"
        else:
            return f"{nombre_valor}_of_{palo}.png"

    def cargar_imagen_carta(self, valor, palo):
        archivo = self.construir_nombre_archivo(valor, palo)
        path = os.path.join("cartas", archivo)
        try:
            imagen = Image.open(path).resize((150, 218))
            return ImageTk.PhotoImage(imagen)
        except FileNotFoundError:
            print(f"Imagen no encontrada: {archivo}")
            return None

    def mostrar_siguiente_carta(self):
        if self.index < len(self.baraja):
            valor, palo = self.baraja[self.index]
            self.carta_img = self.cargar_imagen_carta(valor, palo)
            if self.carta_img:
                self.label_img.config(image=self.carta_img)

            self.cuenta_real += conteo_hi_lo[valor]
            print(f"Carta mostrada: {valor} de {palo}, valor conteo: {conteo_hi_lo[valor]}")
            print(f"Cuenta parcial real: {self.cuenta_real}")

            self.index += 1
            self.root.after(self.tiempo, self.mostrar_siguiente_carta)
        else:
            print(f"Cuenta final: {self.cuenta_real}")
            self.pedir_resultado()

    def pedir_resultado(self):
        self.limpiar_pantalla()
        tk.Label(self.root, text="¿Cuál fue la cuenta final?",
                 font=("Arial", 14), fg="white", bg="darkgreen").pack(pady=20)
        self.entrada = tk.Entry(self.root, font=("Arial", 16), justify='center')
        self.entrada.pack(pady=10)
        self.entrada.focus()

        tk.Button(self.root, text="Enviar", font=("Arial", 14),
                  command=self.verificar_resultado).pack(pady=10)

        # ✅ Activar Enter para enviar respuesta
        self.root.bind("<Return>", lambda event: self.verificar_resultado())

    def verificar_resultado(self):
        try:
            cuenta_usuario = int(self.entrada.get())
        except ValueError:
            messagebox.showerror("Error", "Debes escribir un número")
            return

        if cuenta_usuario == self.cuenta_real:
            messagebox.showinfo("Resultado", "✅ ¡Correcto! ¡Buen trabajo!")
        else:
            messagebox.showinfo("Resultado", f"❌ Incorrecto. La cuenta era {self.cuenta_real}.")

        self.crear_pantalla_inicio()

    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.unbind("<Return>")


# Ejecutar
if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()

