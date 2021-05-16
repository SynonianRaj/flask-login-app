import sqlite3 as sql


class SQL:
    def __init__(self, sq):
        with sq.connect('Mydata.db') as self.sql:
            self.db = self.sql.cursor()

    def execute_cmd(self, *args):
        a = self.db.execute(*args)
        self.sql.commit()
        # self.sql.close()
        return a


db = SQL(sql)
db.execute_cmd('''CREATE TABLE persons (
    firstName,
    lastName,
    email,
    password
)''')


# db.execute_cmd("""DROP TABLE persons""")  # Delete table
