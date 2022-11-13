# mysql - mysql-connector-python

class DBInterface:
    # интерфейс для бд
    def __init__(self, dictic=True):
        self.dictic = dictic
        # for postgres cursor_factory=DictCursor

    def __enter__(self):
        # postgres:  psycopg2.connect
        self.cnx = mysql.connector.connect({
            "user": "user",
            "password": "password",
            "host": "127.0.0.1",
            "port": "3306",
            "database": "calendar",
        })
        self.cursor = self.cnx.cursor(buffered=True, dictionary=self.dictic)
        return self.cursor
    
    def __exit__(self):
        try:
            self.cnx.commit()
            self.cursor.close()
            self.cnx.close()
        except Exception as e:
            logger.error(e)
