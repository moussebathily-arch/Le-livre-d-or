import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",   # ou "db" si Docker
        port="5432",
        database="postgres",
        user="postgres",
        password="1234"
    )
    print("✅ Connexion réussie !")

    conn.close()

except Exception as e:
    print("❌ Erreur :", e)
