import pyautogui
import time
import threading
from tkinter import *

# Variable pour contrôler l'exécution du script
running = False
start_time = None

def update_timer():
    if running and start_time:
        elapsed_time = time.time() - start_time
        timer_label.config(text=f"Temps écoulé : {int(elapsed_time)}s")
    root.after(1000, update_timer)

def start_clicking():
    global running, start_time
    running = True
    start_time = time.time()
    start_button.config(bg='green')
    while running:
        x, y = pyautogui.position()
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown(button='right')
        pyautogui.mouseUp(button='right')
        time.sleep(delay.get())

def stop_clicking():
    global running
    running = False
    start_button.config(bg='red')

def start_thread():
    t = threading.Thread(target=start_clicking)
    t.start()

# Création de l'interface utilisateur
root = Tk()
delay = IntVar()
delay.set(26)
delay_entry = Entry(root, textvariable=delay)
delay_entry.pack()
start_button = Button(root, text='Start', command=start_thread)
start_button.pack()
stop_button = Button(root, text='Stop', command=stop_clicking)
stop_button.pack()
timer_label = Label(root, text="Temps écoulé : 0s")
timer_label.pack()

update_timer()
root.mainloop()
