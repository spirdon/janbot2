import random
import re
import discord

import jb2.command
import jb2.embed


class EloCommand(jb2.command.Command):
    def __init__(self, connector):
        self.connector = connector
        with open('res/text/elo_odpowiedzi.txt') as file:
            self.answers = file.readlines()

    def get_pattern(self):
        return r'elo$'

    async def action(self, prefix, message, client):
        author_m = message.author.mention

        emoji = ":wave:"
        answer = random.choice(self.answers)
        emb = jb2.embed.embed(emoji, author_m, answer)

        await client.send_message(message.channel, embed=emb)
