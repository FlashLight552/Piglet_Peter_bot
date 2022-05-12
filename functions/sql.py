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


    def user_create_table(self):
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS user_data (
                                user_id INT PRIMARY KEY,
                                ds_token VARCHAR(100),
                                lang_bot VARCHAR(20),
                                lang_tts VARCHAR(20) 
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
            
