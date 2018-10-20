import re


class Command:
    def get_pattern(self):
        pass

    async def action(self, connector, message, client):
        pass

    async def process(self, jb2_server, connector, message, client):
        msg = message.content.strip().lower()

        if re.match(jb2_server.prefix + self.get_pattern(), msg) is not None:
            await self.action(jb2_server, connector, message, client)
