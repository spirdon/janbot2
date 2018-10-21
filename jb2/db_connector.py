import os
import urllib
import psycopg2


class DatabaseConnector:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        print("* Trying to connect to database")

        try:
            result = urllib.parse.urlparse(os.getenv('DATABASE_URL'))
            self.conn = psycopg2.connect(
                database=result.path[1:],
                user=result.username,
                password=result.password,
                host=result.hostname
            )
            self.cursor = self.conn.cursor()
            print("** Connected to database")
        except:
            print("** Could not connect to database")

    def execute_sql_file(self, file_path):
        with open(file_path) as f:
            lines = f.readlines()
        
        query = ' '.join(lines)
        queries = query.strip().split(';')
        queries = [q.strip() for q in queries if q.strip() != '']

        for q in queries:
            print("** Execute query:\n" + q.strip())
            self.cursor.execute(q)

    def execute_sql_file_with_args(self, file_path, args):
        with open(file_path) as f:
            lines = f.readlines()
        
        query = ' '.join(lines)

        print("** Execute query:\n" + query.strip())

        self.cursor.execute(query, args)

    def create_tables(self):
        print("* Creating tables (if they don't exist)")
        self.execute_sql_file('res/query/create_tables.sql')
        self.conn.commit()

    def get_server(self, server_id):
        print("* Looking for server ({})".format(server_id))
        self.execute_sql_file_with_args('res/query/find_server.sql', (server_id,))
        rows = self.cursor.fetchall()

        if rows == []:
            print("** Could not find server")
            print("** Adding server to database")
            self.execute_sql_file_with_args('res/query/create_server.sql',
                                            (server_id,))
            self.conn.commit()
            print("** Added server to database")

            return {
                'server_id': server_id,
                'prefix': 'jb2_'
            }

        row = list(rows[0])
        print("** Found server")

        return {
            'server_id': row[0],
            'prefix': row[1]
        }

    def set_server_prefix(self, server_id, prefix):
        self.execute_sql_file_with_args('res/query/set_server_prefix.sql',
                                        (prefix, server_id))
        self.conn.commit()
