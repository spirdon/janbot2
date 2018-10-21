import random
import re
import requests
import discord

from bs4 import BeautifulSoup

import jb2.command
import jb2.embed


class UfnalCommand(jb2.command.Command):
    def __init__(self):
        with open('res/text/ufnalizmy.txt', 'r') as file:
            self.ufnalisms = file.readlines()
        self.load_new_ufnalisms()
        with open('res/text/ufnalizmy.txt', 'w') as file:
            for ufnalism in self.ufnalisms:
                file.write(ufnalism + '\n')

    def get_pattern(self):
        return r'ufnal$'

    async def action(self, connector, message, client):
        footer_text = "Ufnalizm dla " + str(message.author)

        emb = discord.Embed(color=0xd48b1a)
        emb.set_footer(text=footer_text, icon_url=message.author.avatar_url)
        emb.title = ":beer: Losowy ufnalizm"
        emb.description = random.choice(self.ufnalisms)

        await client.send_message(message.channel, embed=emb)

    def load_new_ufnalisms(self):
        last_page = 25

        long_link = "https://steamcommunity.com/profiles/76561198014133816/" +\
                    "allcomments?ctp={}"

        for page in range(last_page):
            try:
                r = requests.get(long_link.format(page))
                data = r.text
                soup = BeautifulSoup(data, "html.parser")
                comment_class = "commentthread_comment_text"
                comments = soup.findAll("div", {"class": comment_class})
                texts = [a for a in comments if a.string is not None]

                for text in texts:
                    self.ufnalisms.append(text.string.strip())
            except Exception:
                print("# Ufnalisms: page {} not found".format(page))

        # Reformat ufnalisms
        for i in range(len(self.ufnalisms)):
            if self.ufnalisms[i][-1] == '\n':
                self.ufnalisms[i] = self.ufnalisms[i][:-1]
            self.ufnalisms[i] = self.ufnalisms[i][:2000].strip()

        # Remove empty lines
        self.ufnalisms = [u for u in self.ufnalisms if u != '']

        # Remove duplicates
        self.ufnalisms = list(set(self.ufnalisms))



