import fdb

# HHH
database = {"host": "192.168.1.100", "database": "flask",
            "user": "SYSDBA", "password": "masterkey"}

# AAA
database_skl = {"host": "192.168.1.100", "database": "sss",
                "user": "SYSDBA", "password": "masterkey"}


class Fdb_Class:
    """
        Take path to base, first and last number fuk and query
    """
    def __init__(self, path_to_base, numbers_of_fak, query) -> None:
        self.path_to_base = path_to_base
        self.number_of_fak = numbers_of_fak
        self.query = query

    def __iter__(self):
        return self

    def con_to_firebird_purchase3(self):
        con = fdb.connect(**self.path_to_base)
        cur = con.cursor()
        try:
            cur.execute(self.query.format(**self.number_of_fak))
        except fdb.Error as e:
            print(e)
        else:
            for line in cur.fetchall():
                yield line
        finally:
            con.close()


if __name__ == "__main__":
    pass
