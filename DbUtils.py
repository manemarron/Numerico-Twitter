import psycopg2
import psycopg2.extras

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

    def fetchone(self, table, columns, condition_values, conditions=None,sort=None):
        cur = self.conn.cursor(cursor_factory= psycopg2.extras.DictCursor)
        columns = ",".join(x for x in tuple(columns))
        sql = "SELECT {1} FROM {0}".format(table, columns)
        if conditions  is not None:
            sql += " WHERE {}".format(" AND ".join(x for x in conditions))
        if sort is not None:
            sql += " ORDER BY {}".format(sort)
        cur.execute(sql, condition_values)
        ret = cur.fetchone()
        cur.close()
        return ret

    def insert(self, table, columns, values, returning=None):
        if len(values) > 0:
            columns = ",".join(x for x in tuple(columns))
            placeholder = ",".join(["%s"] * len(values))

            cur = self.conn.cursor()
            sql = 'INSERT INTO {} ({}) VALUES {}'.format(table, columns, placeholder)
            if returning is not None:
                sql += " RETURNING %s" % returning
            cur.execute(sql, values)
            if returning is not None:
                returning = cur.fetchone()
            self.conn.commit()
            cur.close()
            return returning

    def selsert(self, table, insert_columns, insert_values, returning, select_columns=None, select_values=None):
        select_columns = select_columns or insert_columns
        select_values =  select_values or insert_values
        conditions = ["{}=%s".format(x) for x in select_columns]
        res = self.fetchone(table=table, columns=["*"], condition_values=select_values, conditions=conditions)
        if res is not None:
            ret = res[returning]
        else:
            ret = self.insert(table=table, columns=insert_columns, values=insert_values,returning=returning)[0]
        return ret

    def upsert(self, table, columns, update_columns, values, returning=None):
        if len(values) > 0:
            columns = ",".join(x for x in columns)
            fields = ",".join("{0}=nv.{0}".format(x) for x in update_columns)
            placeholder = ",".join(["%s"] * len(values))

            cur = self.conn.cursor()
            sql = (
                "WITH new_values({columns}) as (values {placeholder})," +
                "upsert as (UPDATE {table} t SET {fields} FROM new_values nv WHERE t.id=nv.id RETURNING t.*)" +
                " INSERT INTO {table}({columns})"
                " SELECT {columns} FROM new_values"
                " WHERE NOT EXISTS (SELECT 1 FROM upsert up WHERE up.id=new_values.id)"
            ).format(table=table, columns=columns, fields=fields, placeholder=placeholder)
            if returning is not None:
                sql += " RETURNING {};".format(returning)
            cur.execute(sql, values)
            if returning is not None:
                returning = cur.fetchall()
            self.conn.commit()
            cur.close()
            return returning
