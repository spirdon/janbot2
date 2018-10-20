import os

import jb2.client
import jb2.db_connector

client = jb2.client.client
connector = jb2.db_connector.DatabaseConnector()
commands = () # TODO fill with commands!


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

    jb2_server = connector.get_server(message.server.id)

    # Process all commands (run them if regex is ok)
    for command in commands:
        await command.process(jb2_server, message, client)


def main():
    try:
        client.run(os.getenv('TOKEN'))
    except Exception as exception:
        print("# Exception: " + str(exception))


if __name__ == "__main__":
    main()
