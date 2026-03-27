import tkinter as tk
import psycopg2
import os

class QuizApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")

        #  Connexion DB
        self.conn = psycopg2.connect(
            host="localhost",  # ou "db" si Docker
            database="guestbook",
            user="guest_user",
            password="guest_pass"
        )

        #  Variable choix utilisateur
        self.selected = tk.StringVar()

        #  Question
        self.q_label = tk.Label(root, text="", font=("Arial", 16), wraplength=400)
        self.q_label.pack(pady=20)

        #  Options
        self.options = []
        for val in ["A", "B", "C", "D"]:
            btn = tk.Radiobutton(
                root,
                text="",
                variable=self.selected,
                value=val,
                font=("Arial", 12)
            )
            btn.pack(anchor="w")
            self.options.append(btn)

        #  Bouton submit
        self.submit_btn = tk.Button(
            root,
            text="Soumettre",
            command=self.check_answer
        )
        self.submit_btn.pack(pady=10)

        #  Charger question
        self.load_question()

    #  Charger question aléatoire
    def load_question(self):
        cur = self.conn.cursor()

        cur.execute("""
            SELECT question, option_a, option_b, option_c, option_d, correct_answer
            FROM questions
            ORDER BY RANDOM()
            LIMIT 1
        """)

        row = cur.fetchone()

        self.current_answer = row[5]

        self.q_label.config(text=row[0])

        # remplir options
        for i, opt in enumerate(row[1:5]):
            self.options[i].config(text=opt)

        self.selected.set("")  # reset choix

    #  Vérifier réponse
    def check_answer(self):
        if self.selected.get() == self.current_answer:
            print(" Bonne réponse !")
        else:
            print(" Mauvaise réponse")

        # charger nouvelle question
        self.load_question()


#  Lancement
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
