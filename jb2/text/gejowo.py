import random
import requests
import discord

from bs4 import BeautifulSoup

import jb2.command
import jb2.embed


class GejowoCommand(jb2.command.Command):
    def get_pattern(self):
        return r'gejowo$'

    async def action(self, connector, message, client):
        footer_text = "Gejowski anons dla " + str(message.author)

        emb = discord.Embed(color=0xff476f)
        emb.set_footer(text=footer_text, icon_url=message.author.avatar_url)
        emb.title = ":rainbow: Gejowski anons"
        emb.description = self.random_ad()

        await client.send_message(message.channel, embed=emb)

    def random_ad(self):
        category = 7
        full_link = "http://anonse.gejowo.pl/?m=list&pg={}&cat={}"
        req = requests.get(full_link.format(1, category))
        data = req.text
        soup = BeautifulSoup(data, "html.parser")
        pagination_div = soup.find("div", {"class": "pagination"})

        try:
            last_page = int(pagination_div.find_all("a")[-2].string)
        except IndexError or ValueError:
            last_page = 1
        
        page = random.randint(1, last_page)
        req = requests.get(full_link.format(page, category))
        data = req.text
        soup = BeautifulSoup(data, "html.parser")
        random_ads = soup.find_all("div", {"class": "adcontent"})
        return random.choice(random_ads).string
