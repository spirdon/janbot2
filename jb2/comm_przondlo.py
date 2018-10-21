import random
import re
import discord

import jb2.command
import jb2.embed


class PrzondloCommand(jb2.command.Command):
    def get_pattern(self):
        return r'przondlo( [.\n\w\d ]+)?$'

    async def action(self, connector, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        pattern = self.get_pattern()

        text = re.match("^" + pattern, msg).group(1)

        if text is None:
            text = "Potrzebny parametr: **text**"
            emb = jb2.embed.error_embed(author_m, text)
        else:
            text = self.__przondling(text.lower().strip())
            emb = discord.Embed()
            emb.description = "{}: {}".format(author_m, text)

        await client.send_message(message.channel, embed=emb)

    def __przondling(self, text):
        przondling_factor = 0.3
        letter_dict = {
            'q': 'qwas',
            'w': 'qweasd',
            'e': 'wresfd',
            'r': 'rtefdg',
            't': 'yrtghf',
            'y': 'uythg',
            'u': 'iuyjkh',
            'i': 'ioukjl',
            'o': 'ipokl;',
            'p': 'pol',
            'a': 'qasz',
            's': 'wsadx',
            'd': 'erdfsxc',
            'f': 'rtdfgcv',
            'g': 'tygfhbv',
            'h': 'uyjghnb',
            'j': 'uikjhmn',
            'k': 'iojklm,',
            'l': 'pokl',
            'z': 'aszx',
            'x': 'sdxzc',
            'c': 'xcv',
            'v': 'bvc',
            'b': 'vbn',
            'n': 'bmn',
            'm': 'mnjkl'
        }
        out = ""
        for l in list(text):
            if l not in letter_dict:
                out += l
                continue
            r = random.uniform(0.0, 1.0)
            if r > 0.05:
                new_text = l
            else:
                new_text = ""
            while True:
                r = random.uniform(0.0, 1.0)
                if r < przondling_factor:
                    r2 = random.choice([1, 2])
                    char = random.choice(list(letter_dict[l]))
                    if r2 == 1:
                        new_text += char
                    else:
                        new_text = char + new_text
                else:
                    break
            out += new_text
        return out

