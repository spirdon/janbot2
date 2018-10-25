import discord

import jb2.command
import jb2.embed


class TopKudosCommand(jb2.command.Command):
    def get_pattern(self):
        return r'top$'

    async def action(self, prefix, message, client):
        server_id = message.server.id
        emb = discord.Embed()

        kudos = self.connector.get_kudos(server_id)

        desc = ''
        for kudo in kudos:
            member = message.server.get_member(kudo[1])
            desc += "{}. **{}** *({})*\n".format(kudo[3], str(member), kudo[2])

        emb = discord.Embed(description=desc)
        emb.title = ":first_place: Ranking kudosów"
        emb.colour = 0x00ffff
        footer_text = "Ranking dla " + str(message.author)
        emb.set_footer(text=footer_text, icon_url=message.author.avatar_url)

        await client.send_message(message.channel, embed=emb)


