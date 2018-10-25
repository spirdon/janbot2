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

        desc = "**Nazwa**: " + server.name + "\n"
        desc += "**Właściciel**: " + server.owner.mention + "\n"
        desc += "**Region**: " + str(server.region) + "\n"
        if server.afk_channel:
            desc += "**Kanał AFK**: " + str(server.afk_channel) + "\n"
        if server.splash:
            desc += "**Hasło**: " + server.splash + "\n"
        desc += "**Kanały**: " + str(len(server.channels)) + "\n"
        desc += "**Członkowie:** " + str(len(server.members)) + "\n"
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
