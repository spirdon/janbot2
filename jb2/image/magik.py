import random
import re
import shutil
import requests
import discord
import cv2

import jb2.command
import jb2.embed

import numpy as np
from PIL import Image, ImageDraw
from tqdm import trange
from scipy.ndimage.filters import convolve


class MagikCommand(jb2.command.Command):
    def get_pattern(self):
        return r'magik( .*)?$'

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
                await self.magik_image(message, client, image_url)
        else:
            await self.magik_image(message, client, url)

    async def magik_image(self, message, client, url):
        url_copy = url.strip().split('?')[0]
        extension = url_copy.split('.')[-1]
        full_path = 'res/temp/image.' + extension

        #try:
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

        img = Image.open(full_path)
        width, height = img.size

        n_width = 150
        w_percent = n_width / width
        n_height = int(height * w_percent)

        img = img.resize((n_width, n_height), Image.ANTIALIAS)
        img.save(full_path)
        scale = 0.5

        img = cv2.imread(full_path)
        out = crop_r(img, scale)
        out = crop_c(out, scale)
        cv2.imwrite(full_path, out)

        img = Image.open(full_path)
        img = img.resize((width, height), Image.ANTIALIAS)
        img.save(full_path)

        await client.send_file(message.channel, full_path)
        #except ValueError:
        #    text = "Nieprawidłowy URL"
        #    emb = jb2.embed.error_embed(message.author.mention, text)
        #    await client.send_message(message.channel, embed=emb)

def calc_energy(img):
    filter_du = np.array([
        [1.0, 2.0, 1.0],
        [0.0, 0.0, 0.0],
        [-1.0, -2.0, -1.0],
    ])
    # This converts it from a 2D filter to a 3D filter, replicating the same
    # filter for each channel: R, G, B
    filter_du = np.stack([filter_du] * 3, axis=2)

    filter_dv = np.array([
        [1.0, 0.0, -1.0],
        [2.0, 0.0, -2.0],
        [1.0, 0.0, -1.0],
    ])
    # This converts it from a 2D filter to a 3D filter, replicating the same
    # filter for each channel: R, G, B
    filter_dv = np.stack([filter_dv] * 3, axis=2)

    img = img.astype('float32')
    convolved = np.absolute(convolve(img, filter_du)) + np.absolute(convolve(img, filter_dv))

    # We sum the energies in the red, green, and blue channels
    energy_map = convolved.sum(axis=2)

    return energy_map

def crop_c(img, scale_c):
    r, c, _ = img.shape
    new_c = int(scale_c * c)

    for i in trange(c - new_c):
        img = carve_column(img)

    return img

def crop_r(img, scale_r):
    img = np.rot90(img, 1, (0, 1))
    img = crop_c(img, scale_r)
    img = np.rot90(img, 3, (0, 1))
    return img


def carve_column(img):
    r, c, _ = img.shape

    M, backtrack = minimum_seam(img)
    mask = np.ones((r, c), dtype=np.bool)

    j = np.argmin(M[-1])
    for i in reversed(range(r)):
        mask[i, j] = False
        j = backtrack[i, j]

    mask = np.stack([mask] * 3, axis=2)
    img = img[mask].reshape((r, c - 1, 3))
    return img

def minimum_seam(img):
    r, c, _ = img.shape
    energy_map = calc_energy(img)

    M = energy_map.copy()
    backtrack = np.zeros_like(M, dtype=np.int)

    for i in range(1, r):
        for j in range(0, c):
            # Handle the left edge of the image, to ensure we don't index a -1
            if j == 0:
                idx = np.argmin(M[i-1, j:j + 2])
                backtrack[i, j] = idx + j
                min_energy = M[i-1, idx + j]
            else:
                idx = np.argmin(M[i - 1, j - 1:j + 2])
                backtrack[i, j] = idx + j - 1
                min_energy = M[i - 1, idx + j - 1]

            M[i, j] += min_energy

    return M, backtrack


