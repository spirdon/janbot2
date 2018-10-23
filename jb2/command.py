import re


class Command:
    def with_prefix(self):
        return True

    def get_pattern(self):
        pass

    async def action(self, connector, message, client):
        pass

    async def process(self, prefix, connector, message, client):
        msg = message.content
        start_index = len(prefix)

        prefix = prefix.replace('$', '\\$')\
                       .replace('^', '\\^')\
                       .replace('[', '\\[')\
                       .replace(']', '\\]')\
                       .replace('(', '\\(')\
                       .replace(')', '\\)')\
                       .replace('.', '\\.')\
                       .replace('+', '\\+')\

        if self.with_prefix():
            full_pattern = "^" + prefix + self.get_pattern()
            msg = message.content[start_index:]
        else:
            full_pattern = "^" + self.get_pattern()

        print(full_pattern, msg, message.content)
        if re.match(full_pattern, msg) is not None:
            await self.action(connector, message, client)
