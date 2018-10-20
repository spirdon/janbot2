import jb2.client
import os

client = jb2.client.client
commands = () # TODO fill with commands!


@client.event
async def on_ready():
    print("Logged in as: " + str(client.user))


@client.event
async def on_message(message):
    # Omit bot responses
    if message.author.bot:
        return

    for command in commands:
        await command.process(message, client)


def main():
    try:
        client.run(os.getenv('TOKEN'))
    except Exception as exception:
        print("Exception: " + str(exception))

if __name__ == "__main__":
    main()
