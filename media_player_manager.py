from gi.repository import GLib
import gi
from time import time

gi.require_version('Playerctl', '2.0')
from gi.repository import Playerctl

class MediaPlayerManager:
    def __init__(self) -> None:
        self.is_failed = False

        try:
            m = Playerctl.PlayerManager()
            for name in m.props.player_names:
                # print('name', x.name)
                if name.name == 'vlc':
                    self.player = Playerctl.Player.new_from_name(name)

            self.last_toggle = time()
        except Exception as e:
            print(e)
            self.is_failed = True


    def toggle_pause(self):
        if time() - self.last_toggle <= 0.4:
            print('rapid toggle warning')
            return

        print('toggle_pause')
        self.last_toggle = time()
        self.player.play_pause()
        # print('status', self.player.props.playback_status)
        # if self.player.props.playback_status == Playerctl.PlaybackStatus.PLAYING:
        #     self.player.pause()
        # else:
        #     self.player.play()

    def get_position(self):
        return self.player.get_position() / 1000000

    def set_position(self, p):
        self.player.set_position(p * 1000000)

    def seek(self, s):
        print('seek', s)
        self.player.seek(s * 1000000)
        

    def get_progress(self):
        return self.player.get_position() / self.player.props.metadata['mpris:length']

    def set_progress(self, p):
        return self.player.set_position(p * self.player.props.metadata['mpris:length']) 

    def set_volume(self, v):
        print('set_volume', v)
        return self.player.set_volume(v)
