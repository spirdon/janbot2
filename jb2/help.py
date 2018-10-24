import discord
import re

import jb2.command
import jb2.embed


class HelpCommand(jb2.command.Command):
    def get_pattern(self):
        return r'help( .*)?$'

    async def action(self, prefix, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        pattern = self.get_full_pattern(prefix)

        prefix = self.connector.get_server(message.server.id)['prefix']

        group = re.match("^" + pattern, msg).group(1)

        if group is None:
            emb = discord.Embed()
            emb.title = "Jan Bot 2"
            emb.description = "Polski bot memiczny."
            emb.add_field(name=":gear: Ustawienia",
                          value=f"`{prefix}help config`")
            emb.add_field(name=":camera_with_flash: Obrazki",
                          value=f"`{prefix}help image`")
            emb.add_field(name=":tools: Różne",
                          value=f"`{prefix}help misc`")
            emb.add_field(name=":pencil2: Tekst",
                          value=f"`{prefix}help text`")
        else:
            group = group.strip()

            if group == "config":
                emb = discord.Embed()
                emb.title = ":gear: Ustawienia - Komendy"
                emb.description = """
                **`{0}toggle anon`** - włączenie/wyłączenie anonimowości kanału

                **`{0}toggle rank`** - włączenie/wyłączenie punktów kanału

                **`{0}prefix <pfx>`** - wyświetlenie/zmiana prefiksu
                `pfx` - nowy prefiks składający się z 1-4 znaków
                """.format(prefix)
            elif group == "image":
                emb = discord.Embed()
                emb.title = ":camera_with_flash: Obrazki - Komendy"
                emb.description = """
                **`{0}cenzo <url>`** - wstawia twarz papieża na inne twarze
                `url` - adres URL obrazka

                **`{0}chajzer`** - postuje losowego Chajzera

                **`{0}dziadzius`** - postuje losowego dziadziusia

                **`{0}sminem`** - postuje losowego Sminema
                """.format(prefix)
            elif group == "misc":
                emb = discord.Embed()
                emb.title = ":tools: Różne - Komendy"
                emb.description = """
                **`{0}ankieta <question>: <options>`** - postuje ankietę
                `question` - pytanie (musi po nim być dwukropek)
                `options` - odpowiedzi oddzielone znakiem plusa (+)
                """.format(prefix)
            elif group == "text":
                emb = discord.Embed()
                emb.title = ":pencil2: Tekst - Komendy"
                emb.description = """
                **`{0}ask <question>`** - odpowiada na zadane pytanie
                odpowiedzią tak/nie
                `question` - pytanie, które chcesz zadać

                **`{0}elo`** - losowe przywitanie

                **`{0}gejowo`** - losowy anons z gejowo.pl

                **`{0}przondlo <text>`** - zmiana tekstu na bełkot
                `text` - tekst, który ma zostać zmieniony na przondłomowę

                **`{0}szkaluj <nick>`** - szkaluje daną osobę
                `nick` - nick osoby szkalowanej

                **`{0}ufnal`** - postuje losowy post Bartka Ufnala
                """.format(prefix)
            else:
                text = "Nieznana grupa komend"
                emb = jb2.embed.error_embed(author_m, text)
                
        await client.send_message(message.channel, embed=emb)
