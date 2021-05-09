import fdb

database = {"host": "192.168.1.100", "database": "flask",
            "user": "SYSDBA", "password": "masterkey"}


def con_to_firebird(query, *args, **kwargs):
    con = fdb.connect(**database)
    cur = con.cursor()
    try:
        cur.execute(query.format(**kwargs), *args)
    except fdb.Error as e:
        print(e)
    else:
        for line in cur.fetchall():
            yield line
    finally:
        con.close()


if __name__ == "__main__":
    pass
