import tkinter as tk
from tkinter import messagebox
import psycopg2

class GuestbookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Livre d'or persistant")

        # Connexion à la base de données
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                port=5432,
                database="guestbook_db",
                user="postgres",
                password="postgres"
            )
            self.cur = self.conn.cursor()
            conn_status = "Connecté"
            status_color = "green"
        except Exception as e:
            print("Erreur de connexion:", e)
            self.conn = None
            self.cur = None
            conn_status = "Déconnecté"
            status_color = "red"

        # Interface utilisateur
        tk.Label(root, text="Livre d'or", font=("Arial", 16)).pack(pady=10)
        self.name_entry = tk.Entry(root, width=30)
        self.name_entry.pack(pady=5)

        tk.Button(root, text="Signer", command=self.save_signature).pack(pady=5)
        tk.Button(root, text="Effacer la base de données", bg="red", fg="white", command=self.clear_db).pack(pady=5)

        # Listbox pour afficher toutes les signatures
        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack(pady=10)

        # État de la connexion
        self.status_lbl = tk.Label(root, text=f"État : {conn_status}", fg=status_color)
        self.status_lbl.pack(pady=5)

        self.refresh_screen()

        # Gestion de la fermeture propre
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def save_signature(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Erreur", "Le nom ne peut pas être vide !")
            return
        try:
            self.cur.execute("INSERT INTO guestbook (name) VALUES (%s) RETURNING id;", (name,))
            inserted_id = self.cur.fetchone()[0]
            self.conn.commit()
            print(f"Nom '{name}' ajouté avec ID {inserted_id}")
            self.refresh_screen()
            self.name_entry.delete(0, tk.END)
        except Exception as e:
            print("Erreur SQL:", e)
            self.conn.rollback()
            messagebox.showerror("Erreur", f"Impossible d'ajouter le nom: {e}")

    def clear_db(self):
        if messagebox.askyesno("Confirmer", "Voulez-vous vraiment effacer toutes les signatures ?"):
            try:
                self.cur.execute("TRUNCATE TABLE guestbook;")
                self.conn.commit()
                self.refresh_screen()
            except Exception as e:
                print("Erreur SQL:", e)
                self.conn.rollback()
                messagebox.showerror("Erreur", f"Impossible de vider la table: {e}")

    def refresh_screen(self):
        self.listbox.delete(0, tk.END)
        if self.cur:
            self.cur.execute("SELECT id, name FROM guestbook ORDER BY id;")
            for row in self.cur.fetchall():
                self.listbox.insert(tk.END, f"{row[0]}. {row[1]}")

    def search_names(self, query):
        if self.cur:
            self.cur.execute("SELECT id, name FROM guestbook WHERE name ILIKE %s;", (f"%{query}%",))
            return self.cur.fetchall()

    def on_close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GuestbookApp(root)
    root.mainloop()
