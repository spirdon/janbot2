import re
import discord

import jb2.command
import jb2.embed


class AnkietaCommand(jb2.command.Command):
    def get_pattern(self):
        return r'ankieta( .*:)?( ?\+.+)*$'

    async def action(self, connector, message, client):
        msg = message.content.strip()
        author_m = message.author.mention
        pattern = self.get_pattern()

        question = re.match("^" + pattern, msg).group(1)
        options = re.match("^" + pattern, msg).group(2)

        correct = False

        if question is None:
            text = "Potrzebny parametr: **question**"
            emb = jb2.embed.error_embed(author_m, text)
        elif options is None:
            text = "Potrzebny parametr: **options**"
            emb = jb2.embed.error_embed(author_m, text)
        else:
            question = question.strip()[:-1]
            options = [a.strip() for a in options.split('+')][1:]

            if len(options) < 2:
                text = "Muszą być przynajmniej 2 opcje wyboru"
                emb = jb2.embed.error_embed(author_m, text)
            elif len(options) > 10:
                text = "Musi być najwyżej 10 opcji wyboru"
                emb = jb2.embed.error_embed(author_m, text)
            else:
                emoji = ":bar_chart:"
                reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', 
                             '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
                description = "\n"

                for i in range(len(options)):
                    description += reactions[i] + " " + options[i] + "\n\n"

                title = emoji + " " + question
                footer = " | Wybierz opcję klikając na reakcję do tego posta"
                emb = discord.Embed(title=title, description=description)
                emb.title = title
                emb.set_footer(text=footer, icon_url=message.author.avatar_url)
                correct = True

        reply = await client.send_message(message.channel, embed=emb)

        if correct:
            for i in range(len(options)):
                await client.add_reaction(reply, reactions[i])
