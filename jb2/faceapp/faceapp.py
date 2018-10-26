import random
import re
import shutil
import requests
import discord
import faces

import jb2.command
import jb2.embed


class FaceappCommand(jb2.command.Command):
    def get_pattern(self):
        return r'faceapp( [a-z_]*)?( .*)?$'

    async def action(self, prefix, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        pattern = self.get_full_pattern(prefix)
        emb = discord.Embed()

        filter_name = re.match("^" + pattern, msg).group(1)
        url = re.match("^" + pattern, msg).group(2)

        if not filter_name:
            text = "Potrzebny parametr: **filter**"
            emb = jb2.embed.error_embed(author_m, text)
            await client.send_message(message.channel, embed=emb)
        elif not url:
            filter_name = filter_name.strip()
            if not message.attachments:
                text = "Potrzebny parametr: **url**"
                emb = jb2.embed.error_embed(author_m, text)
                await client.send_message(message.channel, embed=emb)
            else:
                image_url = message.attachments[0]['url']
                await self.faceapp_image(message, client,
                                         filter_name, image_url)
        else:
            filter_name = filter_name.strip()
            await self.faceapp_image(message, client, filter_name, url)

    async def faceapp_image(self, message, client, filter, url):
        url_copy = url.strip().split('?')[0]
        extension = url_copy.split('.')[-1]
        full_path = 'res/temp/image.' + extension

        try:
            r = requests.get(url, stream=True)
            if r.status_code != 200:
                text = "Nie można było pobrać obrazka"
                emb = jb2.embed.error_embed(message.author.mention, text)
                await client.send_message(message.channel, embed=emb)
                return

            image = faces.FaceAppImage(url=url)

            if filter not in image.filters:
                text = "Podany filtr nie istnieje"
                emb = jb2.embed.error_embed(message.author.mention, text)
                await client.send_message(message.channel, embed=emb)
                return

            out_image = image.apply_filter(filter)

            with open(full_path, 'wb') as f:
                f.write(out_image)

            await client.send_file(message.channel, full_path)
        except faces.ImageHasNoFaces:
            text = "Nie znaleziono twarzy"
            emb = jb2.embed.error_embed(message.author.mention, text)
            await client.send_message(message.channel, embed=emb)
        except faces.BadImageType:
            text = "Nieprawidłowy rodzaj obrazu"
            emb = jb2.embed.error_embed(message.author.mention, text)
            await client.send_message(message.channel, embed=emb)
        except faces.BaseFacesException:
            text = "Coś poszło nie tak"
            emb = jb2.embed.error_embed(message.author.mention, text)
            await client.send_message(message.channel, embed=emb)
        except ValueError as e:
            text = "Nieprawidłowy URL"
            emb = jb2.embed.error_embed(message.author.mention, text)
            await client.send_message(message.channel, embed=emb)
