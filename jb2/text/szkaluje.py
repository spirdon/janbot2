import random
import re
import discord

import jb2.command
import jb2.embed


class SzkalujeCommand(jb2.command.Command):
    def __init__(self, connector):
        with open('res/text/szkalunki.txt') as file:
            self.slanders = file.readlines()

    def get_pattern(self):
        return r'szkaluj( .+)?$'

    async def action(self, prefix, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        pattern = self.get_full_pattern(prefix)

        slandered = re.match("^" + pattern, msg).group(1)

        if slandered in [None, '']:
            text = "Potrzebny parametr: **nick**"
            emb = jb2.embed.error_embed(author_m, text)
        else:
            footer_text = "Szkalunek dla " + str(message.author)

            emb = discord.Embed()
            emb.description = random.choice(self.slanders).format(slandered)
            emb.set_footer(text=footer_text)

        await client.send_message(message.channel, embed=emb)
