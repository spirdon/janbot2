import re
import discord

import jb2.command
import jb2.embed


class ChannelInfoCommand(jb2.command.Command):
    def get_pattern(self):
        return r'channel$'

    async def action(self, prefix, message, client):
        channel = message.channel
        channel_info = self.connector.get_channel(channel.id)

        desc = "**Nazwa**: " + channel.name + "\n"
        desc += "**ID**: " + channel.id + "\n"
        if channel.topic:
            desc += "**Temat**: " + channel.topic + "\n"
        created_at = channel.created_at.strftime('%d.%m.%Y %H:%M:%S')
        desc += "**Utworzono**: " + created_at + "\n"
        desc += "**Anonimowy**: "
        if channel_info['is_anonymous']:
            desc += "tak\n"
        else:
            desc += "nie\n"
        desc += "**Rankingowy**: "
        if channel_info['is_ranked']:
            desc += "tak\n"
        else:
            desc += "nie\n"
        desc += "**Ruletka włączona**: "
        if channel_info['has_roulette']:
            desc += "tak\n"
        else:
            desc += "nie\n"

        emb = discord.Embed(color=0xffffff)
        emb.title = ":information_source: Informacje o kanale"
        emb.description = desc

        await client.send_message(message.channel, embed=emb)
