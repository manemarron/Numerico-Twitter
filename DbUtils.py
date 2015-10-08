import psycopg2

HOST = "localhost"
PORT = 5432
DB_NAME = "numerico"
USER = "numerico"
PASSWORD = "numerico123"


class DbUtils:
    def __init__(self):
        self.conn = psycopg2.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DB_NAME)

    def close(self):
        self.conn.close()

    def insert(self, table, columns, values, returning=None):
        cur = self.conn.cursor()
        sql = "{0}{1}{2}{3}".format(
            "INSERT INTO %s (" % table,
            (",".join(x for x in tuple(columns))),
            ") VALUES ",
            ",".join(["%s"] * len(values))
        )
        if returning is not None:
            sql += " RETURNING %s" % returning
        cur.execute(sql, values)
        if returning is not None:
            returning = cur.fetchone()[0]
        self.conn.commit()
        cur.close()
        return returning
