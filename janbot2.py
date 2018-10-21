import os

import jb2.client
import jb2.db_connector

import jb2.config.prefix
import jb2.image.chajzer
import jb2.image.dziadzius
import jb2.image.cenzo
import jb2.image.sminem
import jb2.help
import jb2.misc.ankieta
import jb2.text.ask
import jb2.text.elo
import jb2.text.przondlo
import jb2.text.szkaluje
import jb2.text.ufnal
#import jb2.video.comm_cenzovid # doesn't work well


client = jb2.client.client
connector = jb2.db_connector.DatabaseConnector()
commands = (
    jb2.config.prefix.PrefixCommand(),
    jb2.image.chajzer.ChajzerCommand(),
    jb2.image.dziadzius.DziadusCommand(),
    jb2.image.cenzo.CenzoCommand(),
    jb2.help.HelpCommand(),
    jb2.misc.ankieta.AnkietaCommand(),
    jb2.text.ask.AskCommand(),
    jb2.text.elo.EloCommand(),
    jb2.text.przondlo.PrzondloCommand(),
    jb2.text.szkaluje.SzkalujeCommand(),
    jb2.text.ufnal.UfnalCommand()
)


@client.event
async def on_ready():
    print("* Logged in as: " + str(client.user))
    connector.connect()
    connector.create_tables()
    print("-------")
    print("* Ready")


@client.event
async def on_server_join(server):
    # Create new server
    connector.get_server(server.id)


@client.event
async def on_message(message):
    # Omit bot responses
    if message.author.bot:
        return

    # Get server prefix
    prefix = connector.get_server(message.server.id)['prefix']

    # Process all commands (run them if regex is ok)
    for command in commands:
        await command.process(prefix, connector, message, client)


def main():
    try:
        client.run(os.getenv('TOKEN'))
    except Exception as exception:
        print("# Exception: " + str(exception))


if __name__ == "__main__":
    main()
