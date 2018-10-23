import re
import requests

from PIL import Image, ImageDraw, ImageFont

import jb2.command
import jb2.config.ranked
import jb2.embed


class RankCommand(jb2.command.Command):
    def __init__(self, connector):
        self.connector = connector
        self.smaller_fnt = ImageFont.truetype('res/font/font.ttf', 25)
        self.regular_fnt = ImageFont.truetype('res/font/font.ttf', 40)
        self.larger_fnt = ImageFont.truetype('res/font/font.ttf', 60)
        self.downloaded_path = 'res/temp/avatar.webp'
        self.avatar_path = 'res/temp/avatar.png'
        self.frame_path = 'res/images/frame.png'
        self.out_path = 'res/temp/profile.png'

    def get_pattern(self):
        return r'rank( <@!?(\d+)>)?$'

    async def action(self, prefix, message, client):
        msg = message.content.strip().lower()
        user_id = re.match(self.get_full_pattern(prefix), msg).group(2)
        server = message.author.server

        if user_id is None:
            user = message.author
        else:
            user_id = user_id.strip()
            user = server.get_member(user_id)

        self.draw_profile(user, server)

        await client.send_file(message.channel, self.out_path)

    def draw_profile(self, user, server):
        if user.avatar_url != '':
            url = user.avatar_url
        else:
            url = user.default_avatar_url

        r = requests.get(url)

        with open(self.downloaded_path, 'wb') as outfile:
            outfile.write(r.content)

        im = Image.open(self.downloaded_path).convert('RGBA')
        im.save(self.avatar_path, 'png')

        avatar = Image.open(self.avatar_path)
        avatar = avatar.resize((140, 140), Image.ANTIALIAS)
        frame = Image.open(self.frame_path).convert('RGBA')

        exp, lvl = self.connector.get_user(server.id, user.id)[2:4]
        nextlvl_exp = jb2.config.ranked.get_required_exp(lvl)
        prevlvl_exp = jb2.config.ranked.get_required_exp(lvl - 1)

        print(nextlvl_exp, prevlvl_exp)

        progress = (exp - prevlvl_exp)/(nextlvl_exp)

        progress_rect_width = progress * 600
        progress_rect_height = 20

        full_username = str(user).split('#')

        name = '#'.join(full_username[:-1])
        identifier = "#" + full_username[-1]

        if name[-1] == 'j':
            name += ' '

        img = Image.new("RGB", (930, 280), (35, 39, 45))

        # Draw username
        draw = ImageDraw.Draw(img, "RGB")
        draw.rectangle([40, 40, 890, 240], fill=(9, 10, 11))
        draw.text((270, 130), name, font=self.regular_fnt,
                  fill=(255, 255, 255))

        # Draw identifier
        size1 = draw.textsize(name, font=self.regular_fnt)[0]
        draw.text((270 + size1, 130), identifier, font=self.regular_fnt,
                  fill=(90, 90, 90))

        # Draw exp/next_lvl_exp
        exp_left = str(exp - prevlvl_exp)
        exp_right = str(nextlvl_exp)
        text = exp_left + "/" + exp_right
        size2 = draw.textsize(text, font=self.smaller_fnt)[0]
        draw.text((870 - size2, 150), text, fill=(90, 90, 90),
                  font=self.smaller_fnt)

        # Draw lvl
        draw.rectangle((270, 190, 870, progress_rect_height + 190),
                       fill=(38, 69, 38))
        draw.rectangle((270, 190, 270 + progress_rect_width,
                        190 + progress_rect_height), fill=(98, 211, 98))
        size3 = draw.textsize(str(lvl), font=self.larger_fnt)[0]
        draw.text((870 - size3, 40), str(lvl), fill=(98, 211, 98),
                  font=self.larger_fnt)

        # Draw lvl text
        text = "poziom"
        size3 += draw.textsize(text, font=self.smaller_fnt)[0] + 15
        draw.text((870 - size3, 72), text, fill=(58, 89, 58),
                  font=self.smaller_fnt)

        # Draw place
        rank = self.connector.get_user_rank(server.id, user.id)
        text = "#" + str(rank)
        size3 += draw.textsize(text, font=self.larger_fnt)[0] + 30
        draw.text((870 - size3, 40), text, fill=(98, 211, 98),
                  font=self.larger_fnt)

        # Draw place text
        text = "miejsce"
        size3 += draw.textsize(text, font=self.smaller_fnt)[0] + 15
        draw.text((870 - size3, 72), text, fill=(58, 89, 58),
                  font=self.smaller_fnt)

        img.paste(avatar, (70, 70), mask=avatar)
        img.paste(frame, (70, 70), mask=frame)

        img.save(self.out_path)
