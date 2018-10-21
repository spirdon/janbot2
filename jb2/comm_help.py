import discord
import re

import jb2.command
import jb2.embed


class HelpCommand(jb2.command.Command):
    def get_pattern(self):
        return r'help( .*)?$'

    async def action(self, connector, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        pattern = self.get_pattern()

        prefix = connector.get_server(message.server.id)['prefix']

        group = re.match("^" + pattern, msg).group(1)

        if group is None:
            emb = discord.Embed()
            emb.title = "Jan Bot 2"
            emb.description = "Polski bot memiczny."
            emb.add_field(name=":hammer: Moderacja",
                          value=f"`{prefix}help moderation`",
                          inline=True)
            emb.add_field(name=":pencil2: Tekst",
                          value=f"`{prefix}help text`",
                          inline=True)
        else:
            group = group.strip()

            if group == "moderation":
                emb = discord.Embed()
                emb.title = ":hammer: Moderacja - Komendy"
                emb.description = """
                    **`{0}prefix <pfx>`**
                    `pfx` - nowy prefiks składający się z 1-4 znaków
                """.format(prefix)
            elif group == "text":
                emb = discord.Embed()
                emb.title = ":pencil2: Tekst - Komendy"
                emb.description = """
                    **`{0}przondlo <text>`**
                    `text` - tekst, który ma zostać zmieniony na przondłomowę
                """.format(prefix)
            else:
                text = "Nieznana grupa komend"
                emb = jb2.embed.error_embed(author_m, text)
                
        await client.send_message(message.channel, embed=emb)
