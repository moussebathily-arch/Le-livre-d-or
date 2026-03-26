import psycopg2

# Connexion à la base PostgreSQL
conn = psycopg2.connect(
    host="localhost",  # ou le nom du conteneur Docker
    port=5432,
    database="guestbook_db",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

# Création de la table guestbook si elle n'existe pas
cur.execute("""
CREATE TABLE IF NOT EXISTS guestbook (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
""")

conn.commit()
cur.close()
conn.close()
print("Table 'guestbook' créée avec succès !")
