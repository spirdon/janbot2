import random
import re
import discord

import jb2.command
import jb2.embed


class ChoiceCommand(jb2.command.Command):
    def get_pattern(self):
        return r'choice( .+)?$'

    async def action(self, prefix, message, client):
        author_m = message.author.mention
        msg = message.content.strip()

        options = re.match("^" + self.get_full_pattern(prefix), msg).group(1)

        if not options:
            text = "Potrzebny parametr: **options**"
            emb = jb2.embed.error_embed(author_m, text)
        else:
            options = [o.strip() for o in options.split(',')]
            emoji = ":radio_button:"
            answer = random.choice(options)
            emb = jb2.embed.embed(emoji, author_m, answer)

        await client.send_message(message.channel, embed=emb)
