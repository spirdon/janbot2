import asyncio
import random
import re
import threading
import time
import requests
import discord

import jb2.command
import jb2.embed


class ToggleRouletteCommand(jb2.command.Command):
    def get_pattern(self):
        return r'toggle roulette$'

    async def action(self, prefix, message, client):
        author_m = message.author.mention

        if message.author.server_permissions.administrator:
            result = self.connector.get_channel(message.channel.id)
            self.connector.toggle_channel_roulette(message.channel.id)
            if result["has_roulette"]:
                text = "Wyłączono losowanie roli"
            else:
                text = "Włączono losowanie roli"
            emb = jb2.embed.success_embed(author_m, text)
        else:
            text = "Aby wykonać tę operację musisz być Administratorem"
            emb = jb2.embed.error_embed(author_m, text)
        await client.send_message(message.channel, embed=emb)


class RouletteTimeCommand(jb2.command.Command):
    def get_pattern(self):
        return r'roulette time( [a-zA-Z0-9_ ]+)?(,)?( ?\d{2,7})?$'

    async def action(self, prefix, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        role_name = re.match("^" + self.get_full_pattern(prefix), msg).group(1)
        comma = re.match("^" + self.get_full_pattern(prefix), msg).group(2)
        role_time = re.match("^" + self.get_full_pattern(prefix), msg).group(3)

        roles = self.connector.get_server_roles(message.server.id)

        if message.author.server_permissions.administrator:
            if not role_name:
                text = "Potrzebny parametr: **role**"
                emb = jb2.embed.error_embed(author_m, text)
            elif not role_time:
                role_name = role_name.strip()
                full_roles = [r for r in roles if r[2] == role_name]
                if not full_roles:
                    text = "Podana rola nie istnieje"
                    emb = jb2.embed.error_embed(author_m, text)
                else:
                    role_time = full_roles[0][4]
                    text = "Czas posiadania roli **{}**: *{} s*"
                    text = text.format(role_name, role_time)
                    emb = jb2.embed.info_embed(author_m, text)
            elif not comma:
                text = "Potrzebny przecinek pomiędzy argumentami"
                emb = jb2.embed.error_embed(author_m, text)
            else:
                role_name = role_name.strip()
                role_time = role_time.strip()
                text = "Ustawiono czas posiadania roli na *{} s*"
                text = text.format(role_time)
                self.connector.set_role_time(message.server.id, role_name,
                                             role_time)
                emb = jb2.embed.success_embed(author_m, text)
        else:
            text = "Aby wykonać tę operację musisz być Administratorem"
            emb = jb2.embed.error_embed(author_m, text)

        await client.send_message(message.channel, embed=emb)


class RouletteAddCommand(jb2.command.Command):
    def get_pattern(self):
        return r'roulette add( [a-zA-Z0-9_ ]+)?$'

    async def action(self, prefix, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        role_name = re.match("^" + self.get_full_pattern(prefix), msg).group(1)

        if message.author.server_permissions.administrator:
            if not role_name:
                text = "Potrzebny parametr: **role**"
                emb = jb2.embed.error_embed(author_m, text)
            else:
                roles = self.connector.get_server_roles(message.server.id)
                role_name = role_name.strip()
                role_names = [r[2] for r in roles]
                role = discord.utils.get(message.server.roles, name=role_name)
                if role_name in role_names or not role:
                    text = "Nie można dodać tej roli: **{}**".format(role_name)
                    emb = jb2.embed.error_embed(author_m, text)
                elif discord.utils.get(message.server.roles, name=role_name):
                    text = "Dodano rolę: **{}**".format(role_name)
                    self.connector.add_role_name(message.server.id,
                                                 message.channel.id,
                                                 role_name)
                    emb = jb2.embed.success_embed(author_m, text)
                else:
                    text = "Dana rola nie istnieje"
                    emb = jb2.embed.error_embed(author_m, text)
        else:
            text = "Aby wykonać tę operację musisz być Administratorem"
            emb = jb2.embed.error_embed(author_m, text)
        await client.send_message(message.channel, embed=emb)


class RouletteDeleteCommand(jb2.command.Command):
    def get_pattern(self):
        return r'roulette delete( [a-zA-Z0-9_ ]+)?$'

    async def action(self, prefix, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        role_name = re.match("^" + self.get_full_pattern(prefix), msg).group(1)

        if message.author.server_permissions.administrator:
            if role_name is None:
                text = "Potrzebny parametr: **role**"
                emb = jb2.embed.error_embed(author_m, text)
            else:
                roles = self.connector.get_server_roles(message.server.id)
                role_name = role_name.strip()
                role_names = [r[2] for r in roles]
                role = discord.utils.get(message.server.roles, name=role_name)
                if role_name not in role_names or not role:
                    text = "Nie można usunąć podanej roli"
                    emb = jb2.embed.error_embed(author_m, text)
                else:
                    text = "Usunięto rolę: **{}**".format(role_name)
                    self.connector.delete_role_name(message.server.id,
                                                    role_name)
                    emb = jb2.embed.success_embed(author_m, text)
        else:
            text = "Aby wykonać tę operację musisz być Administratorem"
            emb = jb2.embed.error_embed(author_m, text)
        await client.send_message(message.channel, embed=emb)


class RouletteStextsCommand(jb2.command.Command):
    def get_pattern(self):
        return r'roulette stexts( [a-zA-Z0-9_ ]+)?(,)?( ?.+)?$'

    async def action(self, prefix, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        role_name = re.match("^" + self.get_full_pattern(prefix), msg).group(1)
        comma = re.match("^" + self.get_full_pattern(prefix), msg).group(2)
        url = re.match("^" + self.get_full_pattern(prefix), msg).group(3)

        roles = self.connector.get_server_roles(message.server.id)

        if message.author.server_permissions.administrator:
            if not role_name:
                text = "Potrzebny parametr: **role**"
                emb = jb2.embed.error_embed(author_m, text)
            elif not url:
                text = "Potrzebny parametr: **url**"
                emb = jb2.embed.error_embed(author_m, text)
            elif not comma:
                text = "Potrzebny przecinek pomiędzy argumentami"
                emb = jb2.embed.error_embed(author_m, text)
            else:
                url = url.strip()
                roles = self.connector.get_server_roles(message.server.id)
                role_name = role_name.strip()
                role_names = [r[2] for r in roles]
                role = discord.utils.get(message.server.roles, name=role_name)
                if role_name not in role_names or not role:
                    text = "Nie można ustawić tekstu do tej roli: **{}**"
                    text = text.format(role_name)
                    emb = jb2.embed.error_embed(author_m, text)
                elif discord.utils.get(message.server.roles, name=role_name):
                    text = "Ustawiono tekst do roli: **{}**".format(role_name)
                    self.connector.set_role_stexts(message.server.id,
                                                   role_name,
                                                   url)
                    emb = jb2.embed.success_embed(author_m, text)
                else:
                    text = "Dana rola nie istnieje"
                    emb = jb2.embed.error_embed(author_m, text)
        else:
            text = "Aby wykonać tę operację musisz być Administratorem"
            emb = jb2.embed.error_embed(author_m, text)

        await client.send_message(message.channel, embed=emb)


class RouletteTextsCommand(jb2.command.Command):
    def get_pattern(self):
        return r'roulette texts( [a-zA-Z0-9_ ]+)?(,)?( ?.+)?$'

    async def action(self, prefix, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        role_name = re.match("^" + self.get_full_pattern(prefix), msg).group(1)
        comma = re.match("^" + self.get_full_pattern(prefix), msg).group(2)
        url = re.match("^" + self.get_full_pattern(prefix), msg).group(3)

        roles = self.connector.get_server_roles(message.server.id)

        if message.author.server_permissions.administrator:
            if not role_name:
                text = "Potrzebny parametr: **role**"
                emb = jb2.embed.error_embed(author_m, text)
            elif not url:
                text = "Potrzebny parametr: **url**"
                emb = jb2.embed.error_embed(author_m, text)
            elif not comma:
                text = "Potrzebny przecinek pomiędzy argumentami"
                emb = jb2.embed.error_embed(author_m, text)
            else:
                url = url.strip()
                roles = self.connector.get_server_roles(message.server.id)
                role_name = role_name.strip()
                role_names = [r[2] for r in roles]
                role = discord.utils.get(message.server.roles, name=role_name)
                if role_name not in role_names or not role:
                    text = "Nie można ustawić tekstu do tej roli: **{}**"
                    text = text.format(role_name)
                    emb = jb2.embed.error_embed(author_m, text)
                elif discord.utils.get(message.server.roles, name=role_name):
                    text = "Ustawiono tekst do roli: **{}**".format(role_name)
                    self.connector.set_role_texts(message.server.id,
                                                  role_name,
                                                  url)
                    emb = jb2.embed.success_embed(author_m, text)
                else:
                    text = "Dana rola nie istnieje"
                    emb = jb2.embed.error_embed(author_m, text)
        else:
            text = "Aby wykonać tę operację musisz być Administratorem"
            emb = jb2.embed.error_embed(author_m, text)

        await client.send_message(message.channel, embed=emb)


class RouletteEtextsCommand(jb2.command.Command):
    def get_pattern(self):
        return r'roulette etexts( [a-zA-Z0-9_ ]+)?(,)?( ?.+)?$'

    async def action(self, prefix, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        role_name = re.match("^" + self.get_full_pattern(prefix), msg).group(1)
        comma = re.match("^" + self.get_full_pattern(prefix), msg).group(2)
        url = re.match("^" + self.get_full_pattern(prefix), msg).group(3)

        roles = self.connector.get_server_roles(message.server.id)

        if message.author.server_permissions.administrator:
            if not role_name:
                text = "Potrzebny parametr: **role**"
                emb = jb2.embed.error_embed(author_m, text)
            elif not url:
                text = "Potrzebny parametr: **url**"
                emb = jb2.embed.error_embed(author_m, text)
            elif not comma:
                text = "Potrzebny przecinek pomiędzy argumentami"
                emb = jb2.embed.error_embed(author_m, text)
            else:
                url = url.strip()
                roles = self.connector.get_server_roles(message.server.id)
                role_name = role_name.strip()
                role_names = [r[2] for r in roles]
                role = discord.utils.get(message.server.roles, name=role_name)
                if role_name not in role_names or not role:
                    text = "Nie można ustawić tekstu do tej roli: **{}**"
                    text = text.format(role_name)
                    emb = jb2.embed.error_embed(author_m, text)
                elif discord.utils.get(message.server.roles, name=role_name):
                    text = "Ustawiono tekst do roli: **{}**".format(role_name)
                    self.connector.set_role_etexts(message.server.id,
                                                   role_name,
                                                   url)
                    emb = jb2.embed.success_embed(author_m, text)
                else:
                    text = "Dana rola nie istnieje"
                    emb = jb2.embed.error_embed(author_m, text)
        else:
            text = "Aby wykonać tę operację musisz być Administratorem"
            emb = jb2.embed.error_embed(author_m, text)

        await client.send_message(message.channel, embed=emb)


class RoleListener:
    def __init__(self, connector, client):
        self.connector = connector
        self.client = client

    async def listen(self):
        time_elapsed = 0
        while True:
            await asyncio.sleep(30)
            time_elapsed += 30
            all_roles = self.connector.get_all_roles()
            roulette_channels = self.connector.get_all_roulette_channels()

            for role in all_roles:
                server_id = role[0]
                channel_id = role[1]
                role_name = role[2]
                owner_id = role[3]

                if not owner_id:
                    continue

                if channel_id not in roulette_channels:
                    continue

                prefix = self.connector.get_server(server_id)['prefix']
                prefix = prefix.replace('\\', '')

                time_end = role[5]
                texts_url = role[7]
                etexts_url = role[8]
                channel = self.client.get_channel(channel_id)
                server = self.client.get_server(server_id)
                owner = server.get_member(owner_id)

                emb = discord.Embed()

                time_ends = time.time() >= time_end

                if not time_ends and time_elapsed >= 3600 * 3:
                    time_elapsed = 0

                    if str(owner.status) == "offline":
                        continue

                    if not texts_url:
                        footer_text = "Zmień domyślny tekst za pomocą " +\
                                      prefix + "roulette texts " + \
                                      "<role_name>, <url>"
                        desc = "Reminder, że <@{}> to **{}**!"
                        desc = desc.format(owner_id, role_name)
                        emb.set_footer(text=footer_text)
                    else:
                        r = requests.get(texts_url)
                        content = r.text.split('\n')
                        rand_text = random.choice(content)
                        desc = rand_text.format("<@{}>".format(owner_id))
                    emb.description = desc
                    emb.title = ":reminder_ribbon: Ruletka"

                    try:
                        await self.client.send_message(channel, embed=emb)
                    except discord.errors.InvalidArgument:
                        print("* Could not send message to channel, removed?")
                elif time_ends:
                    self.connector.set_role_owner(server_id, role_name, '')
                    member = server.get_member(owner_id)

                    role = discord.utils.get(server.roles,
                                             name=role_name)
                    await self.client.remove_roles(member, role)

                    if not etexts_url:
                        footer_text = "Zmień domyślny tekst za pomocą " +\
                                      prefix + "roulette etexts " + \
                                      "<role_name>, <url>"
                        desc = "<@{}> już nie ma roli **{}**!"
                        desc = desc.format(owner_id, role_name)
                        emb.set_footer(text=footer_text)
                    else:
                        r = requests.get(etexts_url)
                        content = r.text.split('\n')
                        rand_text = random.choice(content)
                        desc = rand_text.format("<@{}>".format(owner_id))
                    emb.description = desc
                    emb.title = ":reminder_ribbon: Ruletka"
                    try:
                        await self.client.send_message(channel, embed=emb)
                    except discord.errors.InvalidArgument:
                        print("* Could not send message to channel, removed?")
