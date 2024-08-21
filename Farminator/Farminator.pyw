from tkinter import *  # Importe toutes les classes et fonctions de la bibliothèque tkinter.
import pyautogui  # Importe la bibliothèque pyautogui pour contrôler la souris et le clavier.
import time  # Importe la bibliothèque time pour utiliser les fonctions liées au temps.
import threading  # Importe la bibliothèque threading pour créer et gérer des threads.
import keyboard  # Importe la bibliothèque keyboard pour gérer les raccourcis clavier.


# Variables pour contrôler l'exécution du script
running_click = False  # Variable pour contrôler l'exécution de la boucle de clic.
start_time = None  # Variable pour stocker le moment où le script a commencé à s'exécuter.

def update_timer():
    # Cette fonction met à jour le label du timer toutes les secondes.
    if running_click and start_time:
        elapsed_time = time.time() - start_time
        timer_label.config(text=f"Temps écoulé : {int(elapsed_time)}s")
    root.after(1000, update_timer)

def start_clicking():
    # Cette fonction démarre la boucle de clic.
    global running_click, start_time
    running_click = True
    start_time = time.time()
    start_button.config(bg='green')
    num_clicks_entry.config(state='disabled')  # Désactive l'entrée de texte
    interval_entry.config(state='disabled')  # Désactive l'entrée de texte
    while running_click:
        for _ in range(num_clicks.get()):
            x, y = pyautogui.position()
            pyautogui.click(button='left')
            time.sleep(1)  # Intervalle entre chaque clic
        time.sleep(interval.get())  # Intervalle entre chaque série de clics

def stop_clicking():
    # Cette fonction arrête la boucle de clic.
    global running_click
    running_click = False
    start_button.config(bg='red')
    num_clicks_entry.config(state='normal')  # Réactive l'entrée de texte
    interval_entry.config(state='normal')  # Réactive l'entrée de texte

def start_click_thread():
    # Cette fonction crée un nouveau thread pour la boucle de clic.
    t1 = threading.Thread(target=start_clicking)
    t1.start()

def toggle_start_stop():
    # Cette fonction démarre ou arrête les clics en fonction de leur état actuel.
    global running_click
    if running_click:
        stop_clicking()
    else:
        start_click_thread()


# Création de l'interface utilisateur
root = Tk()  # Crée une nouvelle fenêtre tkinter.

num_clicks = IntVar()  # Crée une variable tkinter pour stocker le nombre de clics.
num_clicks.set(5)  # Définit la valeur par défaut du nombre de clics à 5.
num_clicks_label = Label(root, text="Nombre de clics :")  # Crée un label pour le nombre de clics.
num_clicks_label.pack()  # Ajoute le label à la fenêtre.
num_clicks_entry = Entry(root, textvariable=num_clicks)  # Crée une entrée de texte pour le nombre de clics.
num_clicks_entry.pack()  # Ajoute l'entrée de texte à la fenêtre.

interval = IntVar()  # Crée une variable tkinter pour stocker l'intervalle entre les séries de clics.
interval.set(6)  # Définit la valeur par défaut de l'intervalle à 6 secondes.
interval_label = Label(root, text="Intervalle entre les séries de clics (en secondes) :")  # Crée un label pour l'intervalle.
interval_label.pack()  # Ajoute le label à la fenêtre.
interval_entry = Entry(root, textvariable=interval)  # Crée une entrée de texte pour l'intervalle.
interval_entry.pack()  # Ajoute l'entrée de texte à la fenêtre.

start_button = Button(root, text='Démarrer les clics', command=start_click_thread)  # Crée un bouton pour démarrer les clics.
start_button.pack()  # Ajoute le bouton à la fenêtre.
stop_button = Button(root, text='Arrêter les clics', command=stop_clicking)  # Crée un bouton pour arrêter les clics.
stop_button.pack()  # Ajoute le bouton à la fenêtre.

timer_label = Label(root, text="Temps écoulé : 0s")  # Crée un label pour afficher le temps écoulé depuis le début de l'exécution du script.
timer_label.pack()  # Ajoute le label à la fenêtre.

keyboard.add_hotkey('9', toggle_start_stop)  # Ajoute un raccourci clavier pour la touche 

update_timer()  # Appelle la fonction update_timer pour commencer à mettre à jour le label du timer.
root.mainloop()  # Démarre la boucle principale de tkinter pour afficher la fenêtre et gérer les événements.
