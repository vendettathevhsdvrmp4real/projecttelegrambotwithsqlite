import sqlite3
from config import DATABASE


class DatabaseManager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS feedback (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            telegram_id INTEGER UNIQUE,
                            name TEXT,
                            problem TEXT
                        )''') 
            conn.commit()
        print("База данных успешно создана.")

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()

    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
        
    def save_user(self, telegram_id: int, name: str):
        """Сохраняет имя пользователя, обновляет если уже есть в базе."""
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO feedback (telegram_id, name) VALUES (?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET name=excluded.name
        ''', (telegram_id, name))
        conn.commit()
        conn.close()

    def get_user_name(self, telegram_id):
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()
        cur.execute("SELECT name FROM feedback WHERE telegram_id = ?", (telegram_id,))
        row = cur.fetchone()
        if row:
            # Возвращаем имя как словарь
            return {"telegram_id": telegram_id, "name": row[0]}
        return None
    
    

if __name__ == '__main__':
    manager = DatabaseManager(DATABASE)
    manager.create_tables()