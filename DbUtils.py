__author__ = 'manemarron'
import psycopg2

HOST = "localhost"
PORT = 5432
DB_NAME = "numerico"
USER = "numerico"
PASSWORD = "numerico123"


class DbUtils:
    def __initialize(self):
        self.conn = psycopg2.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DB_NAME)

    def __close(self):
        self.conn.close()

    def insert(self, table, columns, values):
        cur = self.conn.cursor()
        sql = "{0}{1}{2}{3}".format(
            "INSERT INTO %s (" % table,
            (",".join(x for x in tuple(columns))),
            ") VALUES ",
            ",".join(["(%s)"] * len(values)) + ";"
        )
        cur.execute(sql, values)
        cur.close()
