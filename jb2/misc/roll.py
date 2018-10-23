import random
import re
import discord

import jb2.command
import jb2.embed


class RollCommand(jb2.command.Command):
    def get_pattern(self):
        return r'roll( (\d{1,50})( (\d{1,50}))?)?$'

    async def action(self, prefix, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        pattern = self.get_full_pattern(prefix)

        a = re.match("^" + pattern, msg).group(2)
        b = re.match("^" + pattern, msg).group(3)

        if a is None:
            r = random.randint(1, 100)
        elif b is None:
            r = random.randint(1, int(a))
        else:
            r = random.randint(int(a), int(b))

        emoji = ":game_die:"
        emb = jb2.embed.embed(emoji, author_m, r)
        emb.colour = 0xff2222

        await client.send_message(message.channel, embed=emb)
