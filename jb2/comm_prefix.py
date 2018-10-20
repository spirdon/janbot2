import re

import jb2.command
import jb2.embed


class PrefixCommand(jb2.command.Command):
    def get_pattern(self):
        return r'prefix( .{1,4})?$'

    async def action(self, connector, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        pattern = self.get_pattern()

        prefix = re.match("^" + pattern, msg).group(1)

        if prefix is not None:
            prefix = prefix.strip()
            if message.author.server_permissions.administrator:
                connector.set_server_prefix(message.server.id, prefix)
                text = "Zmieniono prefiks: `{}`".format(prefix)
                emb = jb2.embed.success_embed(author_m, text)
            else:
                text = "Aby wykonać tę operację musisz być Administratorem"
                emb = jb2.embed.error_embed(author_m, text)
        else:
            jb2_server = connector.get_server(message.server.id)
            text = "Aktualny prefiks: `{}`".format(jb2_server['prefix'])
            emb = jb2.embed.info_embed(author_m, text)
        await client.send_message(message.channel, embed=emb)
