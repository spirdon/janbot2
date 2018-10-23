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
        self.execute_sql_file_with_args('res/query/find_server.sql',
                                        (server_id,))
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

    def get_channel(self, channel_id):
        print("* Looking for channel ({})")
        self.execute_sql_file_with_args('res/query/find_channel.sql',
                                        (channel_id,))
        rows = self.cursor.fetchall()
        if rows == []:
            print("** Could not find channel")
            print("** Adding server to database")
            self.execute_sql_file_with_args('res/query/create_channel.sql',
                                            (channel_id,))
            self.conn.commit()
            print("** Added channel to database")

            return {
                'channel_id': channel_id,
                'is_anonymous': False,
                'is_ranked': False
            }

        row = list(rows[0])
        print("** Found channel")

        return {
            'channel_id': row[0],
            'is_anonymous': row[1],
            'is_ranked': row[2]
        }

    def toggle_channel_anon(self, channel_id):
        channel_info = self.get_channel(channel_id)
        anon = channel_info['is_anonymous']
        self.execute_sql_file_with_args('res/query/set_channel_anon.sql',
                                        (anon ^ True, channel_id))
        self.conn.commit()
        return anon ^ True

    def toggle_channel_ranked(self, channel_id):
        channel_info = self.get_channel(channel_id)
        ranked = channel_info['is_ranked']
        self.execute_sql_file_with_args('res/query/set_channel_ranked.sql',
                                        (ranked ^ True, channel_id))
        self.conn.commit()
        return ranked ^ True

    def get_all_anon_channels(self):
        self.execute_sql_file('res/query/get_all_anon_channels.sql')
        rows = self.cursor.fetchall()
        anon_channels = []
        for row in rows:
            anon_channels.append(row[0])
        return anon_channels

    def get_all_ranked_channels(self):
        self.execute_sql_file('res/query/get_all_ranked_channels.sql')
        rows = self.cursor.fetchall()
        ranked_channels = []
        for row in rows:
            ranked_channels.append(row[0])
        return ranked_channels

    def get_user(self, server_id, user_id):
        self.execute_sql_file_with_args('res/query/get_user.sql',
                                        (server_id, user_id))
        rows = self.cursor.fetchall()
        if rows:
            return rows[0]
        
        self.execute_sql_file_with_args('res/query/create_user.sql',
                                        (server_id, user_id))
        return (server_id, user_id, 0, 1)

    def set_user_exp(self, exp, lvl, server_id, user_id):
        self.execute_sql_file_with_args('res/query/set_user_exp.sql',
                                        (exp, lvl, server_id, user_id))
        self.conn.commit()

    def get_ranks(self, server_id):
        self.execute_sql_file_with_args('res/query/get_user_rank.sql',
                                        (server_id,))
        rows = self.cursor.fetchall()
        return rows

    def get_user_rank(self, server_id, user_id):
        ranks = self.get_ranks(server_id)
        for rank in ranks:
            if rank[1] == user_id:
                return rank[4]
