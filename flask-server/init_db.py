import sqlite3

connection = sqlite3.connect('tables.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO courses (code, title, info) VALUES (?, ?, ?)", 
            ('FR101', 'Basic French', 'Learn alphabet and numbers')
)

cur.execute("INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)",
            ('jamieflash', 'admin', 1)

)
connection.commit()
connection.close() 