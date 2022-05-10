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
                                port=MARIA_PORT,
                                database=MARIA_DB
                                )
            self.cursor = self.connection.cursor()
        
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")


    def discord_token_create_table(self):
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS discord_token (
                user_id INT PRIMARY KEY,
                ds_token TEXT 
                )""")
            self.connection.commit()


    def discord_token_save(self, user_id, ds_token):
        # self.discord_token_create_table()
        with self.connection:
            self.cursor.execute("""INSERT INTO discord_token (user_id, ds_token)
                                VALUES (?,?) ON DUPLICATE KEY UPDATE ds_token=?
                                """, (user_id, ds_token, ds_token))
            self.connection.commit()


    def discord_token_request(self, user_id):
        # self.discord_token_create_table()
        with self.connection:
            self.cursor.execute("""SELECT ds_token FROM discord_token WHERE user_id=(?)
                """, (user_id, ))
            
            for item in self.cursor:
                token = item 

            return token[0]

            
