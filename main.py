# -*- coding: utf-8 -*-
import sqlite3

DATABASE = 'portfolio.db'

class DB_Manager:
    def __init__(self, database):
        self.database = database
        # Сразу создаем таблицы при инициализации или вызываем метод отдельно
        self.create_tables()

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            # Создаем таблицу навыков
            conn.execute('''CREATE TABLE IF NOT EXISTS skills (
                            skill_id INTEGER PRIMARY KEY,
                            skill_name TEXT NOT NULL
                        )''')
            # Создаем таблицу статусов
            conn.execute('''CREATE TABLE IF NOT EXISTS status (
                            status_id INTEGER PRIMARY KEY,
                            status_name TEXT NOT NULL
                        )''')
            # Создаем таблицу проектов (для полноты картины)
            conn.execute('''CREATE TABLE IF NOT EXISTS projects (
                            project_id INTEGER PRIMARY KEY,
                            project_name TEXT NOT NULL,
                            status_id INTEGER,
                            FOREIGN KEY (status_id) REFERENCES status (status_id)
                        )''')
            conn.commit()

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()

    def __select_data(self, sql, data=tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()

    def default_insert(self):
        # Проверим, не пусты ли таблицы, чтобы не дублировать данные при каждом запуске
        if not self.get_skills():
            skills = [('Python',), ('SQL',), ('API',)]
            self.__executemany('INSERT INTO skills (skill_name) VALUES (?)', skills)
        
        if not self.get_statuses():
            statuses = [('На этапе проектирования',), ('В процессе разработки',), 
                        ('Разработан. Готов к использованию.',), ('Обновлен',), 
                        ('Завершен. Не поддерживается',)]
            self.__executemany('INSERT INTO status (status_name) VALUES (?)', statuses)

    def get_statuses(self):
        return self.__select_data("SELECT * FROM status")

    def get_skills(self):
        return self.__select_data("SELECT * FROM skills")

if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.default_insert()
    
    print("Статусы в базе:")
    print(manager.get_statuses())
    
    print("\nНавыки в базе:")
    print(manager.get_skills())