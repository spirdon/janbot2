import textwrap
import re
import requests

from PIL import Image, ImageDraw, ImageFont

import jb2.command
import jb2.config.ranked
import jb2.embed


class NpcCommand(jb2.command.Command):
    def __init__(self, connector):
        self.connector = connector
        self.regular_fnt = ImageFont.truetype('res/font/font2.ttf', 45)
        self.template_path = 'res/images/npc_template.jpg'
        self.out_path = 'res/temp/npc.png'

    def get_pattern(self):
        return r'npc( .+)?$'

    async def action(self, prefix, message, client):
        msg = message.content.strip().lower()
        text = re.match(self.get_full_pattern(prefix), msg).group(1)
        server = message.author.server
        max_length = 150

        if text is None:
            text = "Potrzebny parametr: **text**"
            emb = jb2.embed.error_embed(message.author.mention, text)
            await client.send_message(message.channel, embed=emb)
            return

        if len(text) > max_length:
            text = "Tekst za długi, maks. {} znaków".format(max_length)
            emb = jb2.embed.error_embed(message.author.mention, text)
            await client.send_message(message.channel, embed=emb)
            return

        self.draw_image(text)

        await client.send_file(message.channel, self.out_path)

    def draw_image(self, text):
        img = Image.open(self.template_path)
        lines = textwrap.wrap(text, width=27)
        draw = ImageDraw.Draw(img, "RGB")

        if lines[0].strip().startswith('>'):
            color = (123, 138, 86)
        else:
            color = (0, 0, 0)

        line_index = 0

        for line in lines:
            line = line.strip()
            draw.text((396, 111 + line_index * 50), line,
                      font=self.regular_fnt, fill=color)
            line_index += 1
        img.save(self.out_path)
