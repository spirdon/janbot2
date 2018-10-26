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
            emb.add_field(name=":man: FaceApp",
                          value=f"`{prefix}help faceapp`")
            emb.add_field(name=":camera_with_flash: Obrazki",
                          value=f"`{prefix}help image`")
            emb.add_field(name=":information_source: Informacyjne",
                          value=f"`{prefix}help info`")
            emb.add_field(name=":tools: Różne",
                          value=f"`{prefix}help misc`")
            emb.add_field(name=":no_entry_sign: NSFW",
                          value=f"`{prefix}help nsfw`")
            emb.add_field(name=":pencil2: Tekst",
                          value=f"`{prefix}help text`")
        else:
            group = group.strip()

            if group == "config":
                emb = discord.Embed()
                emb.title = ":gear: Ustawienia - Komendy"
                emb.description = """
Poniższe komendy wymagają uprawnień administracyjnych.

**`{0}cooldown [<time>]`** - wyświetlenie/zmiana cooldownu na głosowanie
`time` - ustawienie długości cooldownu (w sekundach)

**`{0}toggle anon`** - włączenie/wyłączenie anonimowości kanału

**`{0}toggle rank`** - włączenie/wyłączenie punktów kanału

**`{0}toggle roulette`** - włączenie/wyłączenie ruletki na kanale

**`{0}prefix <pfx>`** - wyświetlenie/zmiana prefiksu
`pfx` - nowy prefiks składający się z 1-4 znaków
                """.format(prefix)
            elif group == "faceapp":
                emb = discord.Embed()
                emb.title = ":man: FaceApp - Komendy"
                emb.description = """
Poniższe komendy wymagają parametru URL albo dołączenia obrazka do wiadomości.

**`{0}faceapp <filter> [<url>]`** - twarz zmodyfikowana przez filtr FaceAppa
`filter` - jeden z podanych filtrów: 
*- smile
- smile_2
- hot
- old
- young
- hollywood
- fun_glasses 
- hitman
- mustache_free
- pan
- heisenberg
- female
- female_2
- male*
`url` - adres URL do obrazka
                """.format(prefix)
            elif group == "image":
                emb = discord.Embed()
                emb.title = ":camera_with_flash: Obrazki - Komendy"
                emb.description = """
**`{0}avatar [<member>]`** - wstawia awatar danego członka

**`{0}cenzo [<url>]`** - wstawia twarz papieża na inne twarze
`url` - adres URL obrazka

**`{0}chajzer`** - postuje losowego Chajzera

**`{0}dziadzius`** - postuje losowego dziadziusia

**`{0}flip [<url>]`** - odbija obrazek w poziomie
`url` - adres URL obrazka

**`{0}flip2 [<url>]`** - odbija obrazek w pionie
`url` - adres URL obrazka

**`{0}mirror [<url>]`** - odbija zewnętrzne połowy obrazka
`url` - adres URL obrazka

**`{0}mirror2 [<url>]`** - odbija wewnętrzne połowy obrazka
`url` - adres URL obrazka

**`{0}npc [<text>]`** - postuje memix z NPC
`text` - tekst który ma zostać wypowiedziany przez NPC

**`{0}sminem`** - postuje losowego Sminema
                """.format(prefix)
            elif group == "info":
                emb = discord.Embed()
                emb.title = ":information_source: Informacyjne - Komendy"
                emb.description = """
**`{0}channel`** - postuje informacje o kanale

**`{0}role <role_name>`** - postuje informacje o roli dodanej do ruletki
`role_name` - nazwa roli, która została dodana do ruletki

**`{0}server`** - postuje informacje o serwerze
                """.format(prefix)
            elif group == "misc":
                emb = discord.Embed()
                emb.title = ":tools: Różne - Komendy"
                emb.description = """
**`{0}ankieta <question>: <options>`** - postuje ankietę
`question` - pytanie (musi po nim być dwukropek)
`options` - odpowiedzi oddzielone znakiem plusa (+)

**`{0}kudo` <member>** - daje kudosa użytkownikowi
`member` - wzmianka użytkownika, który ma dostać kudosa

**`{0}rank [<member>]`** - wyświetla profil użytkownika
`member` - wzmianka użytkownika, którego profil ma zostać wyświetlony

**`{0}ranking`** - wyświetla ranking użytkowników pod względem ilości punktów

**`{0}roll [<a>] [<b>]`** - losuje liczbę między `a` i `b`
`a` - najmniejsza liczba
`b` - największa liczba
Gdy brakuje `a` i `b`, domyślnie losuje się między 1 a 100. Gdy brakuje `b`,
domyślnie losuje się między 1 a `a`.

**`{0}roulette roll <role_name>`** - losuje rolę wśród użytkowników online
`role_name` - nazwa losowanej roli

**`{0}top`** - wyświetla ranking użytkowników pod względem ilości kudosów
                """.format(prefix)
            elif group == "nsfw":
                emb = discord.Embed()
                emb.title = ":no_entry_sign: NSFW - Komendy"
                emb.description = """
**`{0}imgur`** - losowy obrazek z imgur.com (może wylosować zdjęcia 18+)
                """.format(prefix)
            elif group == "text":
                emb = discord.Embed()
                emb.title = ":pencil2: Tekst - Komendy"
                emb.description = """
**`{0}ask <question>`** - odpowiada na zadane pytanie odpowiedzią tak/nie
`question` - pytanie, które chcesz zadać

**`{0}choice <options>`** - wybiera jedną z podanych opcji
`options` - opcje oddzielone przecinkiem

**`{0}elo`** - losowe przywitanie

**`{0}gejowo`** - losowy anons z gejowo.pl

**`{0}przondlo <text>`** - zmiana tekstu na przondłomowę
`text` - tekst, który ma zostać zmieniony na przondłomowę

**`{0}szkaluj <nick>`** - szkaluje daną osobę
`nick` - nick osoby szkalowanej

**`{0}ufnal`** - postuje losowy post Bartka Ufnala
                """.format(prefix)
            else:
                text = "Nieznana grupa komend"
                emb = jb2.embed.error_embed(author_m, text)
                
        await client.send_message(message.channel, embed=emb)
