import re


class Command:
    def get_pattern(self):
        pass

    def get_help(self):
        pass

    async def action(self, message, client):
        pass

    async def process(self, jb2_server, message, client):
        msg = message.content.strip().lower()

        if re.match(jb2_server.prefix + self.get_pattern(), msg) is not None:
            await self.action(message, client)
