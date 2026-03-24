import tkinter as tk

# Fenêtre principale
root = tk.Tk()
root.title("Code Validator")
root.geometry("400x200")

# Label instruction
label = tk.Label(root, text="Enter the Secret Code:")
label.pack(pady=10)

# Champ de saisie (mode mot de passe)
entry = tk.Entry(root, show="*")
entry.pack(pady=10)

# Label résultat
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

#  Fonction de validation
def check_code():
    user_input = entry.get()

    if user_input == "PythonRocks":
        result_label.config(text="ACCESS GRANTED", fg="green")
    else:
        result_label.config(text="WRONG CODE", fg="red")

# Bouton
tk.Button(root, text="Validate", command=check_code).pack(pady=10)

# Lancer app
root.mainloop()
