import random
import re
import time
import requests
import discord

import jb2.command
import jb2.embed


class RouletteCommand(jb2.command.Command):
    def __init__(self, connector):
        super().__init__(connector)
        self.required_members = 1

    def get_pattern(self):
        return r'roulette roll( [a-zA-Z0-9_ ]+)??$'

    async def action(self, prefix, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        role_name = re.match("^" + self.get_full_pattern(prefix), msg).group(1)

        channels = self.connector.get_all_roulette_channels()
        if message.channel.id not in channels:
            text = "Na tym kanale ruletka jest wyłączona"
            emb = jb2.embed.error_embed(author_m, text)
            await client.send_message(message.channel, embed=emb)
            return

        if role_name is None:
            text = "Potrzebny parametr: **role**"
            emb = jb2.embed.error_embed(author_m, text)
        else:
            roles = self.connector.get_server_roles(message.server.id)
            role_names = [r[2] for r in roles]
            role_name = role_name.strip()
            role = discord.utils.get(message.server.roles, name=role_name)

            if role_name not in role_names or not role:
                text = "Nie można wylosować podanej roli"
                emb = jb2.embed.error_embed(author_m, text)
            else:
                stexts_url = [r[6] for r in roles if r[2] == role_name][0]
                owner_id = [r[3] for r in roles if r[2] == role_name][0]

                if owner_id:
                    text = "Osoba z daną rolą jest już wylosowana (<@{}>)"
                    text = text.format(owner_id)
                    emb = jb2.embed.error_embed(author_m, text)
                    await client.send_message(message.channel, embed=emb)
                    return

                members = message.server.members
                m_online = [m for m in members if str(m.status) != "offline"]
                m_online = [m for m in m_online if not m.bot]

                req = self.required_members
                if len(m_online) < req:
                    text = "Potrzeba co najmniej **{}**".format(req) +\
                           " użytkowników online do ruletki"
                    emb = jb2.embed.error_embed(author_m, text)
                else:
                    random_member = random.choice(m_online)
                    await client.add_roles(random_member, role)
                    self.connector.set_role_owner(message.server.id,
                                                  role_name,
                                                  random_member.id)

                    full_role = [r for r in roles if r[2] == role_name][0]
                    time_end = int(full_role[4] + time.time())
                    self.connector.set_role_time_end(message.server.id,
                                                     role_name,
                                                     time_end)
                    self.connector.set_role_channel(message.server.id,
                                                    role_name,
                                                    message.channel.id)

                    emb = discord.Embed()
                    if not stexts_url:
                        prefix = prefix.replace('\\', '')
                        footer_text = "Zmień domyślny tekst za pomocą " +\
                                      prefix + "roulette stexts " + \
                                      "<role_name>, <url>"
                        desc = "{} ma teraz rolę **{}**!"
                        desc = desc.format(random_member.mention, role_name)
                        emb.set_footer(text=footer_text)
                    else:
                        r = requests.get(stexts_url)
                        content = r.text.split('\n')
                        rand_text = random.choice(content)
                        desc = rand_text.format(random_member.mention)
                    emb.description = desc
                    emb.title = ":slot_machine: Ruletka"
        await client.send_message(message.channel, embed=emb)
