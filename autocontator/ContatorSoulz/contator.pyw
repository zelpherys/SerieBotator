import tkinter as tk
import os
import ctypes
import threading
import keyboard
from tkinter import font
from PIL import ImageGrab
import cv2
import numpy as np
import time

class DeathCounter:
    def __init__(self, root):
        self.root = root
        self.root.title("Compteur de Morts")
        self.root.geometry("300x130")
        self.root.configure(bg="black")

        self.root.iconbitmap(default='')

        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        # Commenter les lignes suivantes qui utilisent dwmSetWindowAttribute
        # ctypes.windll.dwmSetWindowAttribute(hwnd, 20, ctypes.byref(ctypes.c_int(2)), ctypes.sizeof(ctypes.c_int(2)))
        # ctypes.windll.dwmSetWindowAttribute(hwnd, 19, ctypes.byref(ctypes.c_int(1)), ctypes.sizeof(ctypes.c_int(1)))

        self.count = self.read_count_from_file()

        self.custom_font = font.Font(family="OptimusPrinceps", size=20)
        self.custom_font_large = font.Font(family="OptimusPrinceps", size=40)

        self.label = tk.Label(root, text="Nombre de Morts:", font=self.custom_font, fg="white", bg="black")
        self.label.pack(pady=5)

        self.count_label = tk.Label(root, text=f"{self.count}", font=self.custom_font_large, fg="white", bg="black")
        self.count_label.pack(pady=5)

        self.root.bind('<KP_Add>', lambda event: self.increment_count())
        self.root.bind('<plus>', lambda event: self.increment_count())
        self.root.bind('<+>', lambda event: self.increment_count())

        threading.Thread(target=self.listen_for_keypress, daemon=True).start()
        threading.Thread(target=self.check_for_death_message, daemon=True).start()

    def increment_count(self):
        self.count += 1
        self.count_label.config(text=f"{self.count}")
        self.write_count_to_file()

    def decrement_count(self):
        if self.count > 0:
            self.count -= 1
            self.count_label.config(text=f"{self.count}")
            self.write_count_to_file()

    def read_count_from_file(self):
        if os.path.exists("count.txt"):
            with open("count.txt", "r") as file:
                return int(file.read())
        else:
            with open("count.txt", "w") as file:
                file.write("0")
            return 0

    def write_count_to_file(self):
        with open("count.txt", "w") as file:
            file.write(str(self.count))

    def listen_for_keypress(self):
        keyboard.add_hotkey('num 9', self.increment_count)

    def check_for_death_message(self):
        templates = []
        asset_dir = os.path.join(os.path.dirname(__file__), 'asset')
        for filename in os.listdir(asset_dir):
            if filename.endswith('.png'):
                template = cv2.imread(os.path.join(asset_dir, filename))
                if template is not None:
                    templates.append(template)
                else:
                    print(f"Erreur de chargement de l'image : {filename}")

        while True:
            screen_width, screen_height = ImageGrab.grab().size
            screenshot = ImageGrab.grab(bbox=(0, screen_height // 2, screen_width, screen_height))  # Capture la moitié inférieure de l'écran
            screenshot = np.array(screenshot)  # Convertir en tableau numpy

            for template in templates:
                res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.32  # Ajuster le seuil de correspondance
                loc = np.where(res >= threshold)
                if len(loc[0]) > 0:
                    print("Image détectée !")  # Ajout d'une impression pour vérifier la détection
                    self.increment_count()
                    break  # Sortir de la boucle si une correspondance est trouvée
            time.sleep(2)

if __name__ == "__main__":
    root = tk.Tk()
    app = DeathCounter(root)
    root.mainloop()
