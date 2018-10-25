import random
import shutil
import requests
import discord

from bs4 import BeautifulSoup

import jb2.command
import jb2.embed


class ImgurCommand(jb2.command.Command):
    def get_pattern(self):
        return r'imgur$'

    async def action(self, prefix, message, client):
        print(message.channel.name)
        if 'nsfw' not in message.channel.name:
            text = "Komenda działa tylko na kanale NSFW."
            emb = jb2.embed.error_embed(message.author.mention, text)
        else:
            footer_text = "Losowy obrazek dla " + str(message.author)

            emb = discord.Embed(color=0x00ff00)
            emb.set_footer(text=footer_text, icon_url=message.author.avatar_url)
            emb.title = ":frame_photo: Losowy obrazek z Imgura"
            emb.set_image(url=self.random_imgur_url())

        await client.send_message(message.channel, embed=emb)

    def generate_image_id(self):
        letters_num = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        letters_num += "0123456789"
        image_id = ""
        for i in range(5):
            image_id += random.choice(letters_num)
        return image_id

    def random_imgur_url(self):      
        while True:
            extensions = ['jpg', 'png', 'gif']
            index = self.generate_image_id()

            for ext in extensions:
                link = "http://i.imgur.com/{}.{}".format(index, ext)
                headers = requests.head(link).headers
                if 'Content-Type' in headers:
                    return link
                else:
                    continue
