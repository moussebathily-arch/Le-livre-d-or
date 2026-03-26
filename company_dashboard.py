import tkinter as tk
import psycopg2

class CompanyApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Company Dashboard")

        #  Connexion DB (UNE SEULE FOIS)
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="1234"
            )
            print(" Connexion réussie")
        except Exception as e:
            print(" Erreur connexion :", e)
            self.conn = None

        #  Listbox (affichage)
        self.listbox = tk.Listbox(root, width=50, height=15)
        self.listbox.pack(pady=10)

        #  Bouton refresh
        self.btn = tk.Button(
            root,
            text="Actualiser la liste",
            command=self.load_programmers
        )
        self.btn.pack(pady=5)

        #  Bouton quitter propre
        self.exit_btn = tk.Button(
            root,
            text="Quitter",
            command=self.close_office
        )
        self.exit_btn.pack(pady=5)

    #  Charger données
    def load_programmers(self):
        if self.conn is None:
            print(" Pas de connexion DB")
            return

        cur = self.conn.cursor()

        # SQL
        cur.execute("SELECT name, language FROM famous_programmers")
        rows = cur.fetchall()

        #  Nettoyer liste
        self.listbox.delete(0, tk.END)

        #  Remplir
        for row in rows:
            self.listbox.insert(tk.END, f"{row[0]} - {row[1]}")

    #  Fermer proprement
    def close_office(self):
        if self.conn:
            self.conn.close()
            print(" Connexion fermée")

        self.root.destroy()


#  Lancement app
if __name__ == "__main__":
    root = tk.Tk()
    app = CompanyApp(root)
    root.mainloop()
