import os

import jb2.client
import jb2.db_connector

import jb2.config.anon
import jb2.config.cooldown
import jb2.config.prefix
import jb2.config.ranked
import jb2.config.roulette
import jb2.faceapp.faceapp
import jb2.image.avatar
import jb2.image.chajzer
import jb2.image.dziadzius
import jb2.image.cenzo
import jb2.image.flip
import jb2.image.magik
import jb2.image.mirror
import jb2.image.sminem
import jb2.info.channel
import jb2.info.role
import jb2.info.server
import jb2.help
import jb2.misc.ankieta
import jb2.misc.kudo
import jb2.misc.rank
import jb2.misc.ranking
import jb2.misc.roll
import jb2.misc.roulette
import jb2.misc.top_kudos
import jb2.nsfw.imgur
import jb2.text.ask
import jb2.text.choice
import jb2.text.elo
import jb2.text.gejowo
import jb2.text.przondlo
import jb2.text.szkaluje
import jb2.text.ufnal
#import jb2.video.comm_cenzovid # doesn't work well


client = jb2.client.client
connector = jb2.db_connector.DatabaseConnector()
commands = (
    jb2.config.anon.AnonimizeCommand(connector),
    jb2.config.anon.ToggleAnonCommand(connector),
    jb2.config.cooldown.CooldownCommand(connector),
    jb2.config.prefix.PrefixCommand(connector),
    jb2.config.ranked.ExpCommand(connector),
    jb2.config.ranked.ToggleRankCommand(connector),
    jb2.config.roulette.ToggleRouletteCommand(connector),
    jb2.config.roulette.RouletteTimeCommand(connector),
    jb2.config.roulette.RouletteAddCommand(connector),
    jb2.config.roulette.RouletteDeleteCommand(connector),
    jb2.config.roulette.RouletteStextsCommand(connector),
    jb2.config.roulette.RouletteTextsCommand(connector),
    jb2.config.roulette.RouletteEtextsCommand(connector),
    jb2.faceapp.faceapp.FaceappCommand(connector),
    jb2.image.avatar.AvatarCommand(connector),
    jb2.image.cenzo.CenzoCommand(connector),
    jb2.image.chajzer.ChajzerCommand(connector),
    jb2.image.dziadzius.DziadusCommand(connector),
    jb2.image.flip.FlipCommand(connector),
    jb2.image.flip.Flip2Command(connector),
    jb2.image.magik.MagikCommand(connector),
    jb2.image.mirror.MirrorCommand(connector),
    jb2.image.mirror.Mirror2Command(connector),
    jb2.image.sminem.SminemCommand(connector),
    jb2.info.channel.ChannelInfoCommand(connector),
    jb2.info.role.RoleInfoCommand(connector),
    jb2.info.server.ServerInfoCommand(connector),
    jb2.help.HelpCommand(connector),
    jb2.misc.ankieta.AnkietaCommand(connector),
    jb2.misc.kudo.KudoCommand(connector),
    jb2.misc.rank.RankCommand(connector),
    jb2.misc.ranking.RankingCommand(connector),
    jb2.misc.roll.RollCommand(connector),
    jb2.misc.roulette.RouletteCommand(connector),
    jb2.misc.top_kudos.TopKudosCommand(connector),
    jb2.nsfw.imgur.ImgurCommand(connector),
    jb2.text.ask.AskCommand(connector),
    jb2.text.choice.ChoiceCommand(connector),
    jb2.text.elo.EloCommand(connector),
    jb2.text.gejowo.GejowoCommand(connector),
    jb2.text.przondlo.PrzondloCommand(connector),
    jb2.text.szkaluje.SzkalujeCommand(connector),
    jb2.text.ufnal.UfnalCommand(connector)
)


@client.event
async def on_ready():
    print("* Logged in as: " + str(client.user))
    connector.connect()
    connector.create_tables()
    print("-------")
    print("* Ready")

    # Start listening to roles
    await jb2.config.roulette.RoleListener(connector, client).listen()


@client.event
async def on_server_join(server):
    # Create new server
    connector.get_server(server.id)


@client.event
async def on_message(message):
    # Omit bot responses
    if message.author.bot:
        return

    # Get server prefix
    prefix = connector.get_server(message.server.id)['prefix']

    # Process all commands (run them if regex is ok)
    for command in commands:
        await command.process(prefix, message, client)


def main():
    try:
        client.run(os.getenv('TOKEN'))
    except Exception as exception:
        print("# Exception: " + str(exception))


if __name__ == "__main__":
    main()
