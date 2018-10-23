import re


class Command:
    def __init__(self, connector):
        self.connector = connector
    
    def with_prefix(self):
        return True

    def get_pattern(self):
        pass

    def get_full_pattern(self, prefix):
        if self.with_prefix():
            return prefix + self.get_pattern()
        else:
            return self.get_pattern()

    async def action(self, prefix, message, client):
        pass

    async def process(self, prefix, message, client):
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

        if re.match(self.get_full_pattern(prefix), msg) is not None:
            await self.action(prefix, message, client)
