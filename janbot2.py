import jb2.client
import os

CLIENT = jb2.client.client

@CLIENT.event
async def on_ready():
    print("Zalogowano jako " + str(CLIENT.user))

def main():
    try:
        CLIENT.run(os.getenv('TOKEN'))
    except Exception as exception:
        print("Exception: " + str(exception))

if __name__ == "__main__":
    main()
