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


    def create_table_user_data(self):
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS user_data (
                                user_id INT PRIMARY KEY,
                                ds_token VARCHAR(100),
                                lang_assistant VARCHAR(20),
                                lang_tts VARCHAR(20),
                                tz VARCHAR(30)
                                )""")
            self.connection.commit()


    def create_table_remind_app(self):
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS remind_app (
                                id MEDIUMINT NOT NULL AUTO_INCREMENT,
                                user_id INT,
                                text VARCHAR(255),
                                date DATETIME,
                                PRIMARY KEY (id)
                )""")
            self.connection.commit()


    def create_table_sub_to_title(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS sub_to_title (
                            id MEDIUMINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            user_id INT,
                            title_name VARCHAR(200),
                            dub_studio VARCHAR(80)
        )""")
        self.connection.commit()

    def create_table_last_anime_update(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS last_anime_update (
                            title_name VARCHAR(200),
                            ep VARCHAR(50),
                            dub_studio VARCHAR(80),
                            life_time DATETIME default (NOW() + INTERVAL 7 DAY)
        )""")
        self.connection.commit()

    def clear_last_anime_update(self):
        self.cursor.execute("""DELETE FROM last_anime_update 
                            WHERE life_time < now()""")

    def add_in_last_anime_update(self, title_name,ep,dub_studio):
        self.cursor.execute("""INSERT INTO last_anime_update (title_name,ep,dub_studio)
                            VALUES(?,?,?)""", (title_name,ep,dub_studio))
        self.connection.commit()
    
    def find_old_from_last_anime_update(self, title_name,ep,dub_studio):
        self.cursor.execute("""SELECT * FROM last_anime_update WHERE
                            title_name=(?) AND ep=(?) AND dub_studio=(?)""", (title_name,ep,dub_studio))
        list = []
        for item in self.cursor:
            list.append(item[0])
        return list

    def sub_to_new_release(self, user_id:str, title_name:str, dub_studio:str):
        self.cursor.execute(f"""INSERT INTO sub_to_title (user_id, title_name, dub_studio)
                            VALUES (?,?,?)""", (user_id, title_name, dub_studio))
        self.connection.commit()

    def unsub_from_new_release(self, user_id:str, title_name:str, dub_studio:str):
        self.cursor.execute(f"""DELETE FROM sub_to_title
                            WHERE user_id=(?) AND title_name=(?) AND dub_studio=(?)""", (user_id, title_name, dub_studio))
        self.connection.commit()

    def select_dub_from_sub_to_title(self, user_id:str, title_name:str)-> str:
        self.cursor.execute(f"""SELECT dub_studio FROM sub_to_title 
                            WHERE user_id=(?) AND title_name=(?)""", (user_id, title_name))
        list = []
        for item in self.cursor:
            list.append(item[0])
        return list

    def select_user_from_sub_to_title(self, title_name:str, dub_studio:str,)-> str:
        self.cursor.execute(f"""SELECT user_id FROM sub_to_title 
                            WHERE dub_studio=(?) AND title_name=(?)""", (dub_studio, title_name))
        list = []
        for item in self.cursor:
            list.append(item[0])
        return list

    def user_data_save(self, user_id:str ,column:str, data:str):
            self.cursor.execute(f"""INSERT INTO user_data (user_id, {column})
                                VALUES (?,?) ON DUPLICATE KEY UPDATE {column}=?
                                """, (user_id, data, data))
            self.connection.commit()


    def user_data_request(self,user_id:str,column:str) -> str:
            self.cursor.execute(f"""SELECT {column} FROM user_data WHERE user_id=(?)
                                """, (user_id, ))
            token = ''
            for item in self.cursor:
                token = item 
            if token:
                return token[0]
    
    
    def remind_app_save(self, user_id, text, date):
            self.cursor.execute("""INSERT INTO remind_app (user_id, text, date)
                    VALUES (?,?,?)""", (user_id, text, date))
            self.connection.commit()


    def remind_app_request(self, time_start, time_stop):
        self.cursor.execute(f"""SELECT user_id, text FROM remind_app
                WHERE date BETWEEN (?) AND (?)""", (time_start, time_stop))

        data = list()
        for item in self.cursor:
            data.append(item)
        return data


    def remind_app_delete(self, time_start, time_stop):
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
            
