import dbus
bus = dbus.SessionBus()
for service in bus.list_names():
    if service.startswith('org.mpris.MediaPlayer2.'):
        player = dbus.SessionBus().get_object(service, '/org/mpris/MediaPlayer2')

        status=player.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus', dbus_interface='org.freedesktop.DBus.Properties')
        print(status)

        metadata = player.Get('org.mpris.MediaPlayer2.Player', 'Metadata', dbus_interface='org.freedesktop.DBus.Properties')
        print(metadata)
        ss = metadata['mpris:length'] / 1000000
        print(f"{int(ss // 60)}:{int(ss% 60)}")
