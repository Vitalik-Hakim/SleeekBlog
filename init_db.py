import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO images (title, link) VALUES (?, ?)",
            ('Bitcoin', 'uploads/bitcoin-logo.png')
            )

connection.commit()
connection.close()
