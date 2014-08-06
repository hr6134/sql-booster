import MySQLdb as mysql

import config


class Connect(object):
    def make_connection(self):
        self.cursor = mysql.connect(user=config.DB_USER, passwd=config.DB_PASSWD, db=config.DB_NAME).cursor()
        self.cursor.execute("SET NAMES utf8")
        return self


if __name__ == "__main__":
    con = Connect()
    con.make_connection().cursor.execute('show tables')
    print(con.cursor.fetchall())