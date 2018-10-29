import datetime
import re
import discord

import jb2.command
import jb2.embed


class RolesCommand(jb2.command.Command):
    def get_pattern(self):
        return r'roles$'

    async def action(self, prefix, message, client):
        author_m = message.author.mention
        server = message.server

        roles = self.connector.get_all_roles_on_server(server.id)

        roles = [r for r in roles if discord.utils.get(server.roles, name=r[2])]

        if not roles:
            text = "Nie znaleziono żadnych ról"
            emb = jb2.embed.error_embed(author_m, text)
        else:
            desc = ", ".join(list(map(lambda x: x[2], roles)))

            emb = discord.Embed()
            emb.title = ":information_source: Lista ról"
            emb.colour = 0x77ff77
            emb.description = desc

        await client.send_message(message.channel, embed=emb)
