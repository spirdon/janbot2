import os

import jb2.client
import jb2.db_connector

import jb2.comm_ankieta
import jb2.comm_ask
import jb2.comm_chajzer
import jb2.comm_dziadzius
import jb2.comm_elo
import jb2.comm_help
import jb2.comm_papiezify
import jb2.comm_prefix
import jb2.comm_przondlo


client = jb2.client.client
connector = jb2.db_connector.DatabaseConnector()
commands = (
    jb2.comm_ankieta.AnkietaCommand(),
    jb2.comm_ask.AskCommand(),
    jb2.comm_chajzer.ChajzerCommand(),
    jb2.comm_dziadzius.DziadusCommand(),
    jb2.comm_elo.EloCommand(),
    jb2.comm_help.HelpCommand(),
    jb2.comm_papiezify.PapiezifyCommand(),
    jb2.comm_prefix.PrefixCommand(),
    jb2.comm_przondlo.PrzondloCommand()
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

    # Process all commands (run them if regex is ok)
    for command in commands:
        await command.process(connector, message, client)


def main():
    try:
        client.run(os.getenv('TOKEN'))
    except Exception as exception:
        print("# Exception: " + str(exception))


if __name__ == "__main__":
    main()
