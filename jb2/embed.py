import discord


def embed(emoji, mention, text):
    desc = "{} {}: {}".format(emoji, mention, text)
    emb = discord.Embed(description=desc)
    return emb


def success_embed(mention, text):
    emoji = ":white_check_mark:"
    return embed(emoji, mention, text)


def error_embed(mention, text):
    emoji = ":x:"
    return embed(emoji, mention, text)


def info_embed(mention, text):
    emoji = ":information_source:"
    return embed(emoji, mention, text)
