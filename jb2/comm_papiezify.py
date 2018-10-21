import random
import re
import urllib.request
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

        if url is None:
            text = "Musisz podać URL obrazka"
            emb = jb2.embed.error_embed(author_m, text)
        else:
            url = url.strip()
            extension = url.split('.')[-1]
            full_path = 'res/images/image.' + extension
            papaj_path = 'res/images/papaj.png'
            cascadePath = 'res/xml/haarcascade_frontalface_default.xml'

            try:
                urllib.request.urlretrieve(url, full_path)
                img = cv2.imread(full_path, cv2.IMREAD_UNCHANGED)
                face_cascade = cv2.CascadeClassifier(cascadePath)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )
                for (x, y, w, h) in faces:
                    img = cv2.imread(full_path, cv2.IMREAD_UNCHANGED)
                    x_o = int(0.1 * w)
                    y_o = int(0.1 * h)

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
                emb = jb2.embed.error_embed(author_m, text)
                await client.send_message(message.channel, embed=emb)
