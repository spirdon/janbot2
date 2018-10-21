import discord
import re

import jb2.command
import jb2.embed


class HelpCommand(jb2.command.Command):
    def get_pattern(self):
        return r'help( .*)?'

    async def action(self, connector, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        pattern = self.get_pattern()

        prefix = connector.get_server(message.server.id)['prefix']

        group = re.match("^" + pattern, msg).group(1)

        if group is None:
            emb = discord.Embed()
            emb.add_field(name=":hammer: Moderacja",
                          value="`{}help moderation`".format(prefix))
        else:
            group = group.strip()

            if group == "moderation":
                emb = discord.Embed()
                emb.title = ":hammer: Moderacja - Komendy"
                emb.description = """
                    **`{0}prefix <pfx>`**
                    `pfx` - nowy prefiks składający się z 1-4 znaków
                """.format(prefix)
            else:
                text = "Nieznana grupa komend"
                emb = jb2.embed.error_embed(author_m, text)
                
        await client.send_message(message.channel, embed=emb)
