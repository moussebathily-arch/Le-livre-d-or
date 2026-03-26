import tkinter as tk
import psycopg2

# Connexion DB
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="1234"
)

# UI
root = tk.Tk()
root.title("Games")

label = tk.Label(root, text="", justify="left")
label.pack()

def load_games_to_ui():
    cur = conn.cursor()
    cur.execute("SELECT * FROM video_games")
    rows = cur.fetchall()

    result = ""
    for game in rows:
        result += f"{game[1]} - Score: {game[2]}\n"

    label.config(text=result)

btn = tk.Button(root, text="Charger des jeux", command=load_games_to_ui)
btn.pack()

root.mainloop()
