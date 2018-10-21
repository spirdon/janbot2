import random
import re
import discord

import jb2.command
import jb2.embed


class DziadusCommand(jb2.command.Command):
    def __init__(self):
        with open('res/text/dziadziusie.txt') as file:
            self.grandpas = file.readlines()

    def get_pattern(self):
        return r'dziadzius$'

    async def action(self, connector, message, client):
        emb = discord.Embed()
        footer_text = "Dziadziuś dla " + str(message.author)
        emb.set_footer(text=footer_text, icon_url=message.author.avatar_url)
        emb.set_image(url=random.choice(self.grandpas))

        await client.send_message(message.channel, embed=emb)
