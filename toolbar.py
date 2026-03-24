import tkinter as tk

# Fenêtre principale
root = tk.Tk()
root.title("Toolbar Example")
root.geometry("600x400")

#  Frame (barre d'outils en haut)
toolbar = tk.Frame(root)
toolbar.pack(side="top", fill="x")

# Boutons
save_btn = tk.Button(toolbar, text="Save")
save_btn.pack(side="left", padx=10, pady=20)

edit_btn = tk.Button(toolbar, text="Edit")
edit_btn.pack(side="left", padx=10, pady=20)

delete_btn = tk.Button(toolbar, text="Delete", bg="red", fg="white")
delete_btn.pack(side="left", padx=10, pady=20)

# Lancer app
root.mainloop()
