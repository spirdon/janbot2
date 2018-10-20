import re


class Command:
    def get_pattern(self):
        pass

    async def action(self, connector, message, client):
        pass

    async def process(self, connector, message, client):
        msg = message.content.strip().lower()
        jb2_server = connector.get_server(message.server.id)

        if re.match(jb2_server.prefix + self.get_pattern(), msg) is not None:
            await self.action(connector, message, client)
