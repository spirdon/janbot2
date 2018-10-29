import datetime
import re
import discord

import jb2.command
import jb2.embed


class RoleInfoCommand(jb2.command.Command):
    def get_pattern(self):
        return r'role( [a-zA-Z0-9_ ]+)?$'

    async def action(self, prefix, message, client):
        author_m = message.author.mention
        role_info = self.connector.get_all_roles()
        role = None
        msg = message.content.strip()

        role_name = re.match("^" + self.get_full_pattern(prefix), msg).group(1)

        if not role_name:
            text = "Potrzebny parametr: **role_name**"
            emb = jb2.embed.error_embed(author_m, text)
        else:
            role_name = role_name.strip()
            role_info = self.connector.get_role(message.server.id, role_name)

            if not role_info:
                text = "Nie można znaleźć podanej roli"
                emb = jb2.embed.error_embed(author_m, text)
            else:
                desc = "**Nazwa**: " + role_name + "\n"
                desc += "**Obecnie posiada**: "
                if role_info[3]:
                    user = message.server.get_member(role_info[3])
                    desc += user.mention + "\n"
                else:
                    desc += "Nikt \n"
                desc += "**Czas posiadania**: " + str(role_info[4]) + " s\n"
                desc += "**Koniec posiadania**:"
                end_time = datetime.datetime.utcfromtimestamp(role_info[5])
                end_time = end_time.strftime('%d.%m.%Y %H:%M:%S')
                desc += end_time + "\n"

                desc += "**Teksty początkowe**: "
                if not role_info[6]:
                    desc += "**brak**\n"
                else:
                    desc += role_info[6] + "\n"

                desc += "**Teksty przypominające**: "
                if not role_info[7]:
                    desc += "**brak**\n"
                else:
                    desc += role_info[7] + "\n"

                desc += "**Teksty końcowe**: "
                if not role_info[8]:
                    desc += "**brak**\n"
                else:
                    desc += role_info[8] + "\n"

                emb = discord.Embed(color=0xffffff)
                emb.title = ":information_source: Informacje o roli"
                emb.description = desc

        await client.send_message(message.channel, embed=emb)
