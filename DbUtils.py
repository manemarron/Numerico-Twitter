import psycopg2
import psycopg2.extras

HOST = "localhost"
# HOST = "numericodb.cm4vsdgnhr3d.us-west-2.rds.amazonaws.com"
PORT = 5432
DB_NAME = "numerico"
USER = "numerico"
PASSWORD = "numerico123"


class DbUtils:
    def __init__(self):
        self.conn = psycopg2.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DB_NAME)
        self.cursor = None

    def fetchone(self, table, columns, condition_values, conditions=None, sort=None):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        columns = ",".join(x for x in tuple(columns))
        sql = "SELECT %s FROM %s" % (columns, table)
        if conditions is not None:
            sql += " WHERE {}".format(" AND ".join(x for x in conditions))
        if sort is not None:
            sql += " ORDER BY {}".format(sort)
        cur.execute(sql, condition_values)
        ret = cur.fetchone()
        cur.close()
        return ret

    def insert(self, table, columns, values, autocommit=False):
        if len(values) > 0:
            columns = ",".join(x for x in tuple(columns))
            placeholder = ",".join(["%s"] * len(values))

            sql = 'INSERT INTO %s (%s) VALUES %s' % (table, columns, placeholder)
            self.cursor.execute(sql, values)
            if autocommit:
                self.cursor.commit()

    def upsert(self, table, columns, update_columns, values, autocommit=False):
        if len(values) > 0:
            columns = ",".join(x for x in columns)
            fields = ",".join("{0}=nv.{0}".format(x) for x in update_columns)
            placeholder = ",".join(["%s"] * len(values))
            sql = (
                "WITH new_values(%(columns)s) as (values %(placeholder)s)," +
                "upsert as (UPDATE %(table)s t SET %(fields)s FROM new_values nv WHERE t.id=nv.id RETURNING t.*)" +
                " INSERT INTO %(table)s (%(columns)s)"
                " SELECT %(columns)s FROM new_values"
                " WHERE NOT EXISTS (SELECT 1 FROM upsert up WHERE up.id=new_values.id)"
            ) % {"table":table, "columns":columns, "fields":fields, "placeholder":placeholder}
            self.cursor.execute(sql, values)
            if autocommit:
                self.cursor.commit()
