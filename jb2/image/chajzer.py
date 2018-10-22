import random
import re
import discord

import jb2.command
import jb2.embed


class ChajzerCommand(jb2.command.Command):
    def __init__(self):
        with open('res/text/chajzery.txt') as file:
            self.chajzers = file.readlines()

    def get_pattern(self):
        return r'chajzer$'

    async def action(self, connector, message, client):
        emb = discord.Embed()
        emb.colour = 0x00ff00
        footer_text = "Chajzer dla " + str(message.author)
        emb.set_footer(text=footer_text, icon_url=message.author.avatar_url)
        emb.set_image(url=random.choice(self.chajzers))

        await client.send_message(message.channel, embed=emb)
