import tkinter as tk

# Créer la fenêtre
root = tk.Tk()
root.title("Color Changer")
root.geometry("400x300")

#  Fonction pour rouge
def turn_red():
    root.configure(bg="red")

#  Fonction pour vert
def turn_green():
    root.configure(bg="green")

# Boutons
tk.Button(root, text="Go Red", command=turn_red).pack(pady=10)
tk.Button(root, text="Go Green", command=turn_green).pack(pady=10)

# Lancer l'app
root.mainloop()
