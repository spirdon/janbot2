import re
import time
import requests

import jb2.command
import jb2.config.ranked
import jb2.embed


class KudoCommand(jb2.command.Command):
    def get_pattern(self):
        return r'kudo( <@!?(\d+)>)?$'

    async def action(self, prefix, message, client):
        msg = message.content.strip().lower()
        user_id = re.match(self.get_full_pattern(prefix), msg).group(2)
        server = message.server
        author_m = message.author.mention

        if user_id is None:
            text = "Potrzebny parametr: **member**"
            emb = jb2.embed.error_embed(author_m, text)
        else:
            if user_id == message.author.id:
                text = "Nie możesz sobie samemu dać kudosa"
                emb = jb2.embed.error_embed(author_m, text)
                await client.send_message(message.channel, embed=emb)
                return


            cooldown_end = self.connector.get_user(server.id,
                                                   message.author.id)[5]

            if cooldown_end > time.time():
                time_diff = int(cooldown_end - time.time())
                td_hours = time_diff // 3600
                td_minutes = (time_diff - td_hours * 3600) // 60
                td_seconds = (time_diff - td_hours * 3600 - td_minutes * 60)
                text = "Możesz dać kudosa za `{}:{}:{}`".format(td_hours,
                                                                td_minutes,
                                                                td_seconds)
                emb = jb2.embed.error_embed(author_m, text)
            else:
                user_id = user_id.strip()
                user = server.get_member(user_id)

                kudos = self.connector.get_user(server.id, user.id)[4]
                kudos += 1
                self.connector.set_user_kudos(kudos, server.id, user.id)

                text = "Kudosy {}: {}".format(user.mention, kudos)
                emb = jb2.embed.embed(":leaves:", author_m, text)

                server_info = self.connector.get_server(server.id)
                cooldown_end = int(time.time() + server_info['cooldown'])
                self.connector.set_user_cooldown_end(cooldown_end,
                                                     server.id,
                                                     message.author.id)

        await client.send_message(message.channel, embed=emb)
