# import dbus
# bus = dbus.SessionBus()
# for service in bus.list_names():
#     if service.startswith('org.mpris.MediaPlayer2.'):
#         player = dbus.SessionBus().get_object(service, '/org/mpris/MediaPlayer2')
#
#         status=player.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus', dbus_interface='org.freedesktop.DBus.Properties')
#         print(status)
#
#         metadata = player.Get('org.mpris.MediaPlayer2.Player', 'Metadata', dbus_interface='org.freedesktop.DBus.Properties')
#         print(metadata)
#         ss = metadata['mpris:length'] / 1000000
#         print(f"{int(ss // 60)}:{int(ss% 60)}")


from gi.repository import GLib
import gi

gi.require_version('Playerctl', '2.0')
from gi.repository import Playerctl

player = Playerctl.Player()
p = player.get_position()
px = player.props.metadata['mpris:length']
# print(Playerctl.list_players())
print(p / px)
# player.set_position(57156000)
# player
# player.seek(156000)

# print(player.get_title())
#
#
# def on_metadata(player, metadata):
#     if 'xesam:artist' in metadata.keys() and 'xesam:title' in metadata.keys():
#         print('Now playing:')
#         print('{artist} - {title}'.format(
#             artist=metadata['xesam:artist'][0], title=metadata['xesam:title']))
#         
#         print(player.get_artist())
#         # if player.get_artist() == 'Farzad Farzin @GoSong.iR':
#         #     # I meant some good music!
#         #     print('nooo')
#         #     player.next()
#
# def on_play(player, status):
#     # player.set_position(50000000)
#     print('Playing at volume {}'.format(player.props.volume))
#
#
# def on_pause(player, status):
#     print('Paused the song: {}'.format(player.get_title()))
#
#
# player.connect('playback-status::playing', on_play)
# player.connect('playback-status::paused', on_pause)
# player.connect('metadata', on_metadata)

# main = GLib.MainLoop()
# main.run()


# from time import sleep
#
# for x in range(10, 50, 10):
#     print(x)
#     print(player.set_position(100000000*x))
#     print('done')
#     sleep(1.5)
