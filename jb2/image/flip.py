import random
import re
import shutil
import requests
import discord

import jb2.command
import jb2.embed

from PIL import Image, ImageDraw


class FlipCommand(jb2.command.Command):
    def get_pattern(self):
        return r'flip( .*)?$'

    async def action(self, prefix, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        pattern = self.get_full_pattern(prefix)
        emb = discord.Embed()

        url = re.match("^" + pattern, msg).group(1)

        if url is None or url == '':
            if not message.attachments:
                text = "Musisz podać URL obrazka"
                emb = jb2.embed.error_embed(author_m, text)
                await client.send_message(message.channel, embed=emb)
            else:
                image_url = message.attachments[0]['url']
                await self.mirror_image(message, client, image_url)
        else:
            await self.mirror_image(message, client, url)

    async def mirror_image(self, message, client, url):
        url_copy = url.strip().split('?')[0]
        extension = url_copy.split('.')[-1]
        full_path = 'res/temp/image.' + extension

        try:
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(full_path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
            else:
                text = "Nie można było pobrać obrazka"
                emb = jb2.embed.error_embed(message.author.mention, text)
                await client.send_message(message.channel, embed=emb)
                raise Exception

            image = Image.open(full_path)

            flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
            image.paste(flipped_image, (0, 0))

            image.save(full_path)

            await client.send_file(message.channel, full_path)
        except ValueError:
            text = "Nieprawidłowy URL"
            emb = jb2.embed.error_embed(message.author.mention, text)
            await client.send_message(message.channel, embed=emb)


class Flip2Command(jb2.command.Command):
    def get_pattern(self):
        return r'flip2( .*)?$'

    async def action(self, prefix, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        pattern = self.get_full_pattern(prefix)
        emb = discord.Embed()

        url = re.match("^" + pattern, msg).group(1)

        if url is None or url == '':
            if not message.attachments:
                text = "Musisz podać URL obrazka"
                emb = jb2.embed.error_embed(author_m, text)
                await client.send_message(message.channel, embed=emb)
            else:
                image_url = message.attachments[0]['url']
                await self.mirror_image(message, client, image_url)
        else:
            url = url.strip().split('?')[0]
            await self.mirror_image(message, client, url)

    async def mirror_image(self, message, client, url):
        extension = url.split('.')[-1]
        full_path = 'res/temp/image.' + extension

        try:
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(full_path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
            else:
                text = "Nie można było pobrać obrazka"
                emb = jb2.embed.error_embed(message.author.mention, text)
                await client.send_message(message.channel, embed=emb)
                raise Exception

            image = Image.open(full_path)

            flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
            image.paste(flipped_image, (0, 0))

            image.save(full_path)

            await client.send_file(message.channel, full_path)
        except ValueError:
            text = "Nieprawidłowy URL"
            emb = jb2.embed.error_embed(message.author.mention, text)
            await client.send_message(message.channel, embed=emb)
