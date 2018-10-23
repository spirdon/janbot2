import re
import requests

from PIL import Image, ImageDraw, ImageFont

import jb2.command
import jb2.config.ranked
import jb2.embed


class RankCommand(jb2.command.Command):
    def __init__(self):
        self.smaller_fnt = ImageFont.truetype('font.ttf', 25)
        self.regular_fnt = ImageFont.truetype('font.ttf', 40)
        self.larger_fnt = ImageFont.truetype('font.ttf', 60)

    def with_prefix(self):
        return False

    def get_pattern(self):
        return r'rank( <@!?(\d+)>)?$'

    async def action(self, connector, message, client):
        user = message.author
        server = message.server

        if user.avatar_url != '':
            url = user.avatar_url
        else:
            url = user.default_avatar_url

        r = requests.get(url)

        with open('avatar.webp', 'wb') as outfile:
            outfile.write(r.content)

        im = Image.open('res/temp/avatar.webp').convert('RGBA')
        im.save('res/temp/avatar.png', 'png')

        avatar = Image.open('res/temp/avatar.png')
        avatar = avatar.resize((140, 140), Image.ANTIALIAS)
        frame = Image.open('res/temp/frame.png').convert('RGBA')

        current_exp, lvl = connector.get_user(server.id, user.id)[2, 3]
        nextlvl_exp = jb2.config.ranked.get_required_exp(lvl + 1)

        if lvl == 1:
            prevlvl_exp = 0
            progress = current_exp / nextlvl_exp
        else:
            prevlvl_exp = jb2.config.ranked.get_required_exp(lvl)
            progress = (current_exp - prevlvl_exp)/(nextlvl_exp - prevlvl_exp)

        progress_rect_width = progress * 600
        progress_rect_height = 20
        name = user.name
        identifier = "#" + user.identifier

        if name.lower()[-1] == 'j':
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
        exp_left = str(current_exp - prevlvl_exp)
        exp_right = str(nextlvl_exp - prevlvl_exp)
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
        rank = get_rank(connector, server.id, user.id)
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

        img.save('res/temp/profile.png')


def get_rank(connector, server_id, user_id):
    return connector.get_rank(server_id, user_id)
