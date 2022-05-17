import mariadb
from config.config import MARIA_PORT, MARIA_USER, MARIA_PASSWD, MARIA_HOST, \
                            MARIA_DB

class Database:
    def __init__(self):
        try:
            self.connection = mariadb.connect(
                                user=MARIA_USER,
                                password=MARIA_PASSWD,
                                host=MARIA_HOST,
                                port=int(MARIA_PORT),
                                database=MARIA_DB
                                )
            self.cursor = self.connection.cursor()
        
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")


    def create_tables(self):
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS user_data (
                                user_id INT PRIMARY KEY,
                                ds_token VARCHAR(100),
                                lang_assistant VARCHAR(20),
                                lang_tts VARCHAR(20) 
                                )""")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS remind_app (
                                id MEDIUMINT NOT NULL AUTO_INCREMENT,
                                user_id INT,
                                text VARCHAR(255),
                                date DATETIME,
                                PRIMARY KEY (id)
                )""")
            self.connection.commit()


    def user_data_save(self, user_id:str ,column:str, data:str):
        # self.discord_token_create_table()
        with self.connection:
            self.cursor.execute(f"""INSERT INTO user_data (user_id, {column})
                                VALUES (?,?) ON DUPLICATE KEY UPDATE {column}=?
                                """, (user_id, data, data))
            self.connection.commit()


    def user_data_request(self,user_id:str,column:str) -> str:
        # self.discord_token_create_table()
        with self.connection:
            self.cursor.execute(f"""SELECT {column} FROM user_data WHERE user_id=(?)
                                """, (user_id, ))
            token = ''
            for item in self.cursor:
                token = item 
            if token:
                return token[0]
    
    
    def remind_app_save(self, user_id, text, date):
        with self.connection:
            self.cursor.execute("""INSERT INTO remind_app (user_id, text, date)
                    VALUES (?,?,?)""", (user_id, text, date))
            self.connection.commit()


    def remind_app_request(self, time_start, time_stop):
        with self.connection:
            self.cursor.execute(f"""SELECT user_id, text FROM remind_app
                    WHERE date BETWEEN (?) AND (?)""", (time_start, time_stop))

            data = list()
            for item in self.cursor:
                data.append(item)
            return data


    def remind_app_delete(self, time_start, time_stop):
        with self.connection:
            self.cursor.execute("""DELETE FROM remind_app
                    WHERE date BETWEEN (?) AND (?)""", (time_start, time_stop))
            self.connection.commit()

    def sql_request(self, sql:str):
        with self.connection:
            try:
                self.cursor.execute(f"""{sql}""")
            except mariadb.Error as e:
                return e    
            try:
                self.connection.commit()
            except: pass    
            
            list = []
            try:
                for item in self.cursor:
                    list.append(item)    
                return list    
            except: 
                return list
            
