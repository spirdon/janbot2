import datetime
import random
import re
import discord

import jb2.command
import jb2.embed


class ToggleAnonCommand(jb2.command.Command):
    def get_pattern(self):
        return r'toggle anon$'

    async def action(self, prefix, message, client):
        author_m = message.author.mention

        if message.author.server_permissions.administrator:
            result = self.connector.get_channel(message.channel.id)
            self.connector.toggle_channel_anon(message.channel.id)
            if result["is_anonymous"]:
                text = "Ustawiono kanał na jawny"
            else:
                text = "Ustawiono kanał na anonimowy"
            emb = jb2.embed.success_embed(author_m, text)
        else:
            text = "Aby wykonać tę operację musisz być Administratorem"
            emb = jb2.embed.error_embed(author_m, text)
        await client.send_message(message.channel, embed=emb)


class AnonimizeCommand(jb2.command.Command):
    def __init__(self, connector):
        self.connector = connector
        self.pseudos = {}
        with open('res/text/banowalne.txt') as f:
            self.bannable = f.readlines()
        with open('res/text/nicki.txt') as f:
            self.nicks = f.readlines()
        with open('res/text/slowofiltry.txt') as f:
            self.wordfilters = []
            for line in f.readlines():
                k, v = line.split('|')
                self.wordfilters.append((k, v))
        self.colors = (
            0xff5050, 0x50ff50, 0x5050ff,
            0x50ffff, 0xff50ff, 0xffff50,
            0xaa5050, 0x50aa50, 0x5050aa,
            0x50aaaa, 0xaa50aa, 0xaaaa50
        )

    def with_prefix(self):
        return False

    def get_pattern(self):
        return r'(.+)$'

    async def action(self, prefix, message, client):
        if message.channel.id not in self.connector.get_all_anon_channels():
            return
    
        author_id = message.author.id
        msg = message.content.strip()
        await client.delete_message(message)

        if message.author.id not in self.pseudos:
            self.pseudos[author_id] = {
                'name': random.choice(self.nicks),
                'color': random.choice(self.colors)
            }
        name = self.pseudos[message.author.id]['name']
        color = self.pseudos[message.author.id]['color']
        print("msg:", msg)
        text = re.match("^" + self.get_full_pattern(prefix), msg).group(1)
        print("text:", text)
        for wf in self.wordfilters:
            pattern = re.compile(wf[0], re.IGNORECASE)
            text = pattern.sub(wf[1].replace('\\', ''), text)
        if any(word in text for word in self.bannable):
            text += "\n\n**(USER WAS BANNED FOR THIS POST)**"
        emb = discord.Embed(title=name, colour=color, description=text,
                            timestamp=datetime.datetime.now())

        await client.send_message(message.channel, embed=emb)

