import re
import requests
import discord

import jb2.command


class AvatarCommand(jb2.command.Command):
    def get_pattern(self):
        return r'avatar( <@!?(\d+)>)?$'

    async def action(self, prefix, message, client):
        msg = message.content.strip().lower()
        user_id = re.match(self.get_full_pattern(prefix), msg).group(2)
        server = message.author.server

        if user_id is None:
            user = message.author
        else:
            user_id = user_id.strip()
            user = server.get_member(user_id)

        avatar_url = self.get_avatar_url(user)

        emb = discord.Embed()
        emb.set_footer(text="Awatar dla " + str(message.author),
                       icon_url=self.get_avatar_url(message.author))
        emb.set_image(url=avatar_url)

        await client.send_message(message.channel, embed=emb)

    def get_avatar_url(self, user):
        if user.avatar_url != '':
            url = user.avatar_url
        else:
            url = user.default_avatar_url
        return url
