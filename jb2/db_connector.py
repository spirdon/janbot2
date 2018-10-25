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

        if not rows:
            print("** Could not find server")
            print("** Adding server to database")
            self.execute_sql_file_with_args('res/query/create_server.sql',
                                            (server_id,))
            self.conn.commit()
            print("** Added server to database")

            return {
                'server_id': server_id,
                'prefix': 'jb2_',
                'cooldown': 21600
            }

        row = list(rows[0])
        print("** Found server")

        return {
            'server_id': row[0],
            'prefix': row[1],
            'cooldown': row[2]
        }

    def set_server_prefix(self, server_id, prefix):
        self.execute_sql_file_with_args('res/query/set_server_prefix.sql',
                                        (prefix, server_id))
        self.conn.commit()

    def set_server_cooldown(self, cooldown, server_id):
        self.execute_sql_file_with_args('res/query/set_server_cooldown.sql',
                                        (cooldown, server_id,))
        self.conn.commit()

    def get_channel(self, channel_id):
        print("* Looking for channel ({})")
        self.execute_sql_file_with_args('res/query/find_channel.sql',
                                        (channel_id,))
        rows = self.cursor.fetchall()
        if not rows:
            print("** Could not find channel")
            print("** Adding server to database")
            self.execute_sql_file_with_args('res/query/create_channel.sql',
                                            (channel_id,))
            self.conn.commit()
            print("** Added channel to database")

            return {
                'channel_id': channel_id,
                'is_anonymous': False,
                'is_ranked': False,
                'has_roulette': False
            }

        row = list(rows[0])
        print("** Found channel")

        return {
            'channel_id': row[0],
            'is_anonymous': row[1],
            'is_ranked': row[2],
            'has_roulette': row[3]
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

    def toggle_channel_roulette(self, channel_id):
        channel_info = self.get_channel(channel_id)
        roulette = channel_info['has_roulette']
        self.execute_sql_file_with_args('res/query/set_channel_roulette.sql',
                                        (roulette ^ True, channel_id))
        self.conn.commit()
        return roulette ^ True

    def get_all_anon_channels(self):
        self.execute_sql_file('res/query/get_all_anon_channels.sql')
        rows = self.cursor.fetchall()
        return [r[0] for r in rows]

    def get_all_ranked_channels(self):
        self.execute_sql_file('res/query/get_all_ranked_channels.sql')
        rows = self.cursor.fetchall()
        return [r[0] for r in rows]

    def get_all_roulette_channels(self):
        self.execute_sql_file('res/query/get_all_roulette_channels.sql')
        rows = self.cursor.fetchall()
        return [r[0] for r in rows]

    def get_user(self, server_id, user_id):
        self.execute_sql_file_with_args('res/query/get_user.sql',
                                        (server_id, user_id))
        rows = self.cursor.fetchall()
        if rows:
            return rows[0]

        self.execute_sql_file_with_args('res/query/create_user.sql',
                                        (server_id, user_id))
        return (server_id, user_id, 0, 0, 0)

    def set_user_exp(self, exp, lvl, server_id, user_id):
        self.execute_sql_file_with_args('res/query/set_user_exp.sql',
                                        (exp, lvl, server_id, user_id))
        self.conn.commit()

    def set_user_kudos(self, kudos, server_id, user_id):
        self.execute_sql_file_with_args('res/query/set_user_kudos.sql',
                                        (kudos, server_id, user_id))
        self.conn.commit()

    def set_user_cooldown_end(self, cooldown_end, server_id, user_id):
        self.execute_sql_file_with_args('res/query/set_user_cooldown_end.sql',
                                        (cooldown_end, server_id, user_id))
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
        return None

    def set_role_time(self, server_id, role_name, role_time):
        self.execute_sql_file_with_args('res/query/set_role_time.sql',
                                        (role_time, server_id, role_name))
        self.conn.commit()

    def add_role_name(self, server_id, channel_id, role_name):
        self.execute_sql_file_with_args('res/query/add_role_name.sql',
                                        (server_id, channel_id, role_name))
        self.conn.commit()

    def delete_role_name(self, server_id, role_name):
        self.execute_sql_file_with_args('res/query/delete_role_name.sql',
                                        (role_name, server_id))
        self.conn.commit()

    def set_role_owner(self, server_id, role_name, owner_id):
        self.execute_sql_file_with_args('res/query/set_role_owner.sql',
                                        (owner_id, server_id, role_name))
        self.conn.commit()

    def set_role_channel(self, server_id, role_name, channel_id):
        self.execute_sql_file_with_args('res/query/set_role_channel.sql',
                                        (channel_id, server_id, role_name))
        self.conn.commit()

    def get_server_roles(self, server_id):
        self.execute_sql_file_with_args('res/query/get_server_roles.sql',
                                        (server_id,))
        rows = self.cursor.fetchall()
        return rows

    def set_role_time_end(self, server_id, role_name, time_end):
        self.execute_sql_file_with_args('res/query/set_role_time_end.sql',
                                        (time_end, server_id, role_name))
        self.conn.commit()

    def set_role_stexts(self, server_id, role_name, url):
        self.execute_sql_file_with_args('res/query/set_role_stexts.sql',
                                        (url, server_id, role_name))
        self.conn.commit()

    def set_role_texts(self, server_id, role_name, url):
        self.execute_sql_file_with_args('res/query/set_role_texts.sql',
                                        (url, server_id, role_name))
        self.conn.commit()

    def set_role_etexts(self, server_id, role_name, url):
        self.execute_sql_file_with_args('res/query/set_role_etexts.sql',
                                        (url, server_id, role_name))
        self.conn.commit()

    def get_all_roles(self):
        self.execute_sql_file('res/query/get_all_roles.sql')
        return self.cursor.fetchall()

    def get_role(self, server_id, role_name):
        self.execute_sql_file_with_args('res/query/get_role.sql',
                                        (server_id, role_name))
        rows = self.cursor.fetchall()
        if rows:
            return rows[0]
        return None
