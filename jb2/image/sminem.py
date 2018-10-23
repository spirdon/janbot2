import random
import re
import discord

import jb2.command
import jb2.embed


class SminemCommand(jb2.command.Command):
    def __init__(self, connector):
        with open('res/text/sminemy.txt') as file:
            self.sminems = file.readlines()

    def get_pattern(self):
        return r'sminem$'

    async def action(self, prefix, message, client):
        emb = discord.Embed()
        emb.colour = 0x7777ff
        footer_text = "Sminem dla " + str(message.author)
        emb.set_footer(text=footer_text, icon_url=message.author.avatar_url)
        emb.set_image(url=random.choice(self.sminems))

        await client.send_message(message.channel, embed=emb)
