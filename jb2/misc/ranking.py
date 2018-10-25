import re
import requests
import discord

import jb2.command
import jb2.embed


class RankingCommand(jb2.command.Command):
    def get_pattern(self):
        return r'ranking$'

    async def action(self, prefix, message, client):
        server_id = message.server.id
        emb = discord.Embed()

        ranks = self.connector.get_ranks(server_id)

        desc = ''
        for rank in ranks:
            member = message.server.get_member(rank[1])
            desc += "{}. **{}** *({})*\n".format(rank[4], str(member), rank[2])

            if rank[4] > 100:
                break

        emb = discord.Embed(description=desc)
        emb.title = ":star: Ranking poziomów"
        emb.colour = 0x00ffff
        footer_text = "Ranking dla " + str(message.author)
        emb.set_footer(text=footer_text, icon_url=message.author.avatar_url)

        await client.send_message(message.channel, embed=emb)


