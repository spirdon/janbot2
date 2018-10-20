import os

import jb2.client
import jb2.db_connector

import jb2.comm_prefix


client = jb2.client.client
connector = jb2.db_connector.DatabaseConnector()
commands = (
    jb2.comm_prefix.PrefixCommand(),
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
