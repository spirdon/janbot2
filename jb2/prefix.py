import re

import jb2.command
import jb2.embed

class PrefixCommand(jb2.command.Command):
    def get_pattern(self):
        return r'prefix( .{1,4})'

    async def action(self, connector, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        prefix = re.match(self.get_pattern(), msg).group(1)
        if prefix is not None:
            if message.author.server_permissions.administrator:
                text = "Zmieniono prefiks: `{}`".format(prefix)
                emb = jb2.embed.SuccessEmbed(author_m, text)
            else:
                text = "Aby wykonać tę operację musisz być Administratorem"
                emb = jb2.embed.ErrorEmbed(author_m, text)
        else:
            jb2_server = connector.get_server(message.server.id)
            text = "Aktualny prefiks: `{}`".format(jb2_server.prefix)
            emb = jb2.embed.InfoEmbed(author_m, text)
        await client.message.send_message(embed=emb)
