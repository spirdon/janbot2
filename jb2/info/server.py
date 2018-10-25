import re
import discord

import jb2.command
import jb2.embed


class ServerInfoCommand(jb2.command.Command):
    def get_pattern(self):
        return r'server$'

    async def action(self, prefix, message, client):
        server = message.server
        server_info = self.connector.get_server(server.id)
        members = server.members
        a_members = [m for m in members if m.server_permissions.administrator]
        a_members = [m for m in a_members if m is not server.owner]

        desc = "**Nazwa**: " + server.name + "\n"
        desc = "**ID**: " + server.id + "\n"
        desc += "**Właściciel**: " + server.owner.mention + "\n"
        created_at = server.created_at.strftime('%d.%m.%Y %H:%M:%S')
        desc += "**Utworzono**: " + created_at + "\n"
        desc += "**Region**: " + str(server.region) + "\n"
        if server.afk_channel:
            desc += "**Kanał AFK**: " + str(server.afk_channel) + "\n"
        if server.splash:
            desc += "**Hasło**: " + server.splash + "\n"
        desc += "**Kanały**: " + str(len(server.channels)) + "\n"
        desc += "**Członkowie:** " + str(len(members)) + "\n"
        if a_members:
            desc += "**Administratorzy:** "
            for m in a_members:
                    desc += m.mention + " "
            desc += "\n"
        desc += "**Prefiks**: `" + server_info['prefix'] + "`\n"

        desc += "**Emoji**:\n"
        for e in server.emojis:
            desc += str(e)
        emb = discord.Embed(color=0xffffff)
        emb.title = ":information_source: Informacje o serwerze"
        emb.description = desc
        if server.icon_url:
            emb.set_thumbnail(url=server.icon_url)

        await client.send_message(message.channel, embed=emb)
