import random
import re
import discord

import jb2.command
import jb2.embed


class AskCommand(jb2.command.Command):
    def __init__(self):
        with open('res/text/answers.txt') as file:
            self.answers = file.readlines()

    def get_pattern(self):
        return r'ask( .+)?$'

    async def action(self, connector, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        pattern = self.get_pattern()

        question = re.match("^" + pattern, msg).group(1)

        if question is None:
            text = "Potrzebny parametr: **question**"
            emb = jb2.embed.error_embed(author_m, text)
        else:
            emoji = ":8ball:"
            emb = jb2.embed.embed(emoji, author_m, random.choice(self.answers))
            emb.colour = 0x007777

        await client.send_message(message.channel, embed=emb)
