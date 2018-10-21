import re


class Command:
    def get_pattern(self):
        pass

    async def action(self, connector, message, client):
        pass

    async def process(self, connector, message, client):
        msg = message.content
        jb2_server = connector.get_server(message.server.id)
        prefix = jb2_server['prefix']
        start_index = len(prefix)

        prefix = prefix.replace('$', '\\$')\
                       .replace('^', '\\^')\
                       .replace('[', '\\[')\
                       .replace(']', '\\]')\
                       .replace('(', '\\(')\
                       .replace(')', '\\)')\
                       .replace('.', '\\.')

        if re.match("^" + prefix + self.get_pattern(), msg) is not None:
            message.content = message.content[start_index:]
            await self.action(connector, message, client)
