import asyncio
import random
import re
import threading
import time
import requests
import discord

import jb2.command
import jb2.embed


class CooldownCommand(jb2.command.Command):
    def get_pattern(self):
        return r'cooldown( ?\d{2,7})?$'

    async def action(self, prefix, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        new_cd = re.match("^" + self.get_full_pattern(prefix), msg).group(1)

        server_info = self.connector.get_server(message.server.id)

        if message.author.server_permissions.administrator:
            if not new_cd:
                cooldown = server_info['cooldown']
                text = "Cooldown: **{} s**".format(cooldown)
                emb = jb2.embed.info_embed(author_m, text)
            else:
                text = "Ustawiono cooldown na **{} s**"
                text = text.format(new_cd)
                self.connector.set_server_cooldown(message.server.id, new_cd)
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
        while True:
            all_roles = self.connector.get_all_roles()
            roulette_channels = self.connector.get_all_roulette_channels()

            for role in all_roles:
                server_id = role[0]
                channel_id = role[1]
                role_name = role[2]
                owner_id = role[3]

                prefix = self.connector.get_server(server_id)['prefix']
                prefix = prefix.replace('\\', '')

                if channel_id not in roulette_channels:
                    continue

                time_end = role[5]
                texts_url = role[7]
                etexts_url = role[8]
                channel = self.client.get_channel(channel_id)
                server = self.client.get_server(server_id)

                emb = discord.Embed()

                if time.time() < time_end:
                    if not texts_url:
                        footer_text = "Zmień domyślny tekst za pomocą " +\
                                      prefix + "roulette texts " + \
                                      "<role_name>, <url>"
                        desc = "Godzinny reminder, że <@{}> to **{}**!"
                        desc = desc.format(owner_id, role_name)
                        emb.set_footer(text=footer_text)
                    else:
                        r = requests.get(texts_url)
                        content = r.text.split('\n')
                        rand_text = random.choice(content)
                        desc = rand_text.format("<@{}>".format(owner_id))
                    emb.description = desc
                    emb.title = ":reminder_ribbon: Ruletka"
                    await self.client.send_message(channel, embed=emb)
                elif owner_id:
                    self.connector.set_role_owner(server_id,
                                                  role_name,
                                                  '')
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
                    await self.client.send_message(channel, embed=emb)
            await asyncio.sleep(3600)
