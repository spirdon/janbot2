import random
import re
import shutil
import requests
import cv2
import discord

import jb2.command
import jb2.embed

from PIL import Image, ImageDraw


class PapiezifyCommand(jb2.command.Command):
    def get_pattern(self):
        return r'papiezify( .*)?$'

    async def action(self, connector, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        pattern = self.get_pattern()
        emb = discord.Embed()

        url = re.match("^" + pattern, msg).group(1)

        if url is None or url == '':
            if not message.attachments:
                text = "Musisz podać URL obrazka"
                emb = jb2.embed.error_embed(author_m, text)
                await client.send_message(message.channel, embed=emb)
            else:
                image_url = message.attachments[0]['url']
                await self.papiezify(message, client, image_url)
        else:
            url = url.strip().split('?')[0]
            await self.papiezify(message, client, url)

    async def papiezify(self, message, client, url):
        extension = url.split('.')[-1]
        full_path = 'res/images/image.' + extension
        papaj_path = 'res/images/papaj.png'
        cascade_path = 'res/xml/haarcascade_frontalface_default.xml'

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

            img = cv2.imread(full_path, cv2.IMREAD_UNCHANGED)
            face_cascade = cv2.CascadeClassifier(cascade_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            for (x, y, w, h) in faces:
                x_o = int(0.15 * w)
                y_o = int(0.2 * h)

                image = Image.open(full_path)
                papaj = Image.open(papaj_path)

                papaj = papaj.resize((w + x_o * 2,
                                      h + y_o * 2),
                                     Image.ANTIALIAS)

                image.paste(papaj, (x - x_o, y - y_o), mask=papaj)
                image.save(full_path)
            
            await client.send_file(message.channel, full_path)
        except ValueError:
            text = "Nieprawidłowy URL"
            emb = jb2.embed.error_embed(message.author.mention, text)
            await client.send_message(message.channel, embed=emb)
