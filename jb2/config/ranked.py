import jb2.command
import jb2.embed


class ToggleRankCommand(jb2.command.Command):
    def get_pattern(self):
        return r'toggle rank$'

    async def action(self, connector, message, client):
        author_m = message.author.mention

        if message.author.server_permissions.administrator:
            result = connector.get_channel(message.channel.id)
            connector.toggle_channel_anon(message.channel.id)
            if result["is_ranked"]:
                text = "Włączono zdobywanie punktów"
            else:
                text = "Wyłączono zdobywanie punktów"
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

    async def action(self, connector, message, client):
        if message.channel.id not in connector.get_all_ranked_channels():
            return

        msg = message.content.strip()
        author_m = message.author.mention
        prefix = connector.get_server(message.server.id)['prefix']

        # Omit messages that are too long
        if len(msg) > 50:
            return

        # Omit messages that are commands
        if msg.startswith(prefix):
            return
        
        current_exp, current_lvl = connector.get_user_exp(message.server.id,
                                                          message.channel.id)
        exp_added = len(msg)

        exp = current_exp + exp_added
        lvl = self.get_lvl_from_exp(exp)

        connector.set_user_exp(exp, lvl, message.server.id, message.channel.id)

        if lvl > current_lvl:
            text = "Gratulacje, zdobyłeś {} poziom!".format(lvl)
            emb = jb2.embed.embed("::", author_m, text)
            await client.send_message(message.channel, embed=emb)

    def get_lvl_from_exp(self, exp):
        current_lvl = 1
        while self.get_required_exp(current_lvl) < exp:
            current_lvl += 1
        return current_lvl
        
    def get_required_exp(self, lvl):
        current_lvl = 2
        required_exp = 100
        while lvl > current_lvl:
            current_lvl += 1
            required_exp += (current_lvl ** 1.1) * 150
        return int(required_exp)
