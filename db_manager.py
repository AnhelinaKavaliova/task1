import mysql.connector

class DBManager:
    def __init__(self, host, user, password, database):
        self.mydb = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database
        )

        self.mycursor = self.mydb.cursor()

    def execute_query(self, query, params=None):
        self.mycursor.execute(query, params)
        return self.fetch_all()

    def fetch_all(self):
        return self.mycursor.fetchall()
    
    def commit(self):
        return self.mydb.commit()
    
    def close(self):
        self.mycursor.close()
        self.mydb.close()

    