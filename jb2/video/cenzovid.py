import random
import re
import shutil
import requests
import cv2
import discord

import jb2.command
import jb2.embed

from PIL import Image, ImageDraw


class CenzovidCommand(jb2.command.Command):
    def __init__(self):
        self.is_running = False

    def get_pattern(self):
        return r'cenzovid( .*)?$'

    async def action(self, connector, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        pattern = self.get_pattern()
        emb = discord.Embed()

        if self.is_running:
            text = "Obecnie przetwarzany jest filmik, spróbuj później"
            emb = jb2.embed.error_embed(author_m, text)
            await client.send_message(message.channel, embed=emb)

        url = re.match("^" + pattern, msg).group(1)

        if url is None or url == '':
            if not message.attachments:
                text = "Musisz podać URL pliku wideo"
                emb = jb2.embed.error_embed(author_m, text)
                await client.send_message(message.channel, embed=emb)
            else:
                image_url = message.attachments[0]['url']
                await self.papiezify(message, client, image_url)
        else:
            url = url.strip().split('?')[0]
            await self.papiezify(message, client, url)
        self.is_running = False

    async def papiezify(self, message, client, url):
        self.is_running = True
        extension = url.split('.')[-1]

        if extension not in ['mp4', 'webm']:
            text = "Wspierane rozszerzenia to MP4 i WEBM"
            emb = jb2.embed.error_embed(message.author.mention, text)
            await client.send_message(message.channel, embed=emb)
            return

        full_path = 'res/video/movie.' + extension
        frame_path = 'res/images/frame.png'
        papaj_path = 'res/images/papaj.png'
        cascade_path = 'res/xml/haarcascade_frontalface_default.xml'

        try:
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(full_path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
            else:
                text = "Nie można było pobrać pliku wideo"
                emb = jb2.embed.error_embed(message.author.mention, text)
                await client.send_message(message.channel, embed=emb)
                raise Exception

            face_cascade = cv2.CascadeClassifier(cascade_path)
            images = []

            vidcap = cv2.VideoCapture(full_path)
            fps = vidcap.get(cv2.CAP_PROP_FPS)

            print(fps)

            success, image = vidcap.read()
            success = True
            papaj = Image.open(papaj_path)
            width, height = int(vidcap.get(3)), int(vidcap.get(4))
            max_frames = 200

            text = "Tworzenie filmiku może trochę potrwać..."
            emb = jb2.embed.warning_embed(message.author.mention, text)
            await client.send_message(message.channel, embed=emb)

            while success:
                image = cv2.resize(image, (0, 0), fx=1, fy=1)
                images.append(image)
                
                if len(images) > max_frames:
                    txt = f"Ucinanie filmiku do pierwszych {max_frames} klatek"
                    emb = jb2.embed.warning_embed(message.author.mention, txt)
                    await client.send_message(message.channel, embed=emb)
                    break

                success, image = vidcap.read()

            output_path = 'res/video/output.' + extension
            if extension == 'mp4':
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            if extension == 'webm':
                fourcc = cv2.VideoWriter_fourcc(*'vp90')
            video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            count = 0

            for image in images:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )

                cv2.imwrite(frame_path, image)

                for (x, y, w, h) in faces:
                    x_o = int(0.15 * w)
                    y_o = int(0.2 * h)

                    image = Image.open(frame_path)

                    papaj = papaj.resize((w + x_o * 2,
                                          h + y_o * 2),
                                         Image.ANTIALIAS)

                    image.paste(papaj, (x - x_o, y - y_o), mask=papaj)
                    image.save(frame_path)
                image = cv2.imread(frame_path)
                count += 1
                print(str(int(count / len(images) * 100)) + "%", end='\r')
                video.write(image)

            video.release()

            await client.send_file(message.channel, output_path)
        except ValueError:
            text = "Nieprawidłowy URL"
            emb = jb2.embed.error_embed(message.author.mention, text)
            await client.send_message(message.channel, embed=emb)
