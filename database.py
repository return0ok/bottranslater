import sqlite3




database = sqlite3.connect('tranlater.db')
cursor = database.cursor()



cursor.execute('''
    CREATE TABLE IF NOT EXISTS history(
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        from_lang VARCHAR(30),
        to_lang VARCHAR(30),
        original_text TEXT,
        tranlated_text TEXT
    )
''')

database.commit()
cursor.close()
database.close()