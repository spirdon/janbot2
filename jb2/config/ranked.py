import jb2.command
import jb2.embed


class ToggleRankCommand(jb2.command.Command):
    def get_pattern(self):
        return r'toggle rank$'

    async def action(self, prefix, message, client):
        author_m = message.author.mention

        if message.author.server_permissions.administrator:
            result = self.connector.get_channel(message.channel.id)
            self.connector.toggle_channel_ranked(message.channel.id)
            if result["is_ranked"]:
                text = "Wyłączono zdobywanie punktów"
            else:
                text = "Włączono zdobywanie punktów"
            emb = jb2.embed.success_embed(author_m, text)
        else:
            text = "Aby wykonać tę operację musisz być Administratorem"
            emb = jb2.embed.error_embed(author_m, text)
        await client.send_message(message.channel, embed=emb)


class ExpCommand(jb2.command.Command):
    def with_prefix(self):
        return False

    def get_pattern(self):
        return r'(.+)$'

    async def action(self, prefix, message, client):
        if message.channel.id not in self.connector.get_all_ranked_channels():
            return

        msg = message.content.strip()
        author_m = message.author.mention
        prefix = self.connector.get_server(message.server.id)['prefix']
        server_id = message.server.id
        user_id = message.author.id

        # Omit messages that are too long
        if len(msg) > 50:
            return

        # Omit messages that are commands
        if msg.startswith(prefix):
            return

        c_exp, c_lvl = self.connector.get_user(server_id, user_id)[2:4]
        exp_added = len(msg)

        exp = c_exp + exp_added
        lvl = get_lvl_from_exp(exp)

        self.connector.set_user_exp(exp, lvl, server_id, user_id)

        if lvl > c_lvl:
            text = "Gratulacje, zdobyłeś {} poziom!".format(lvl)
            emb = jb2.embed.embed(":star:", author_m, text)
            await client.send_message(message.channel, embed=emb)


def get_lvl_from_exp(exp):
    current_lvl = -1
    while get_required_exp(current_lvl) <= exp:
        current_lvl += 1
    return current_lvl


def get_required_exp(lvl):
    if lvl == -1:
        return 0
    if lvl == 0:
        return 1
    if lvl == 1:
        return 100 + get_required_exp(lvl - 1)
    return get_required_exp(lvl - 1) + int((lvl ** 1.1) * 150)
