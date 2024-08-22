from ssh_terminal_manager import default_collections


class ActionKey(default_collections.ActionKey):
    ...


class ActionName(default_collections.ActionName):
    ...


class SensorKey(default_collections.SensorKey):
    BATOCERA_VERSION = "batocera_version"
    AUDIO_VOLUME = "audio_volume"
    AUDIO_MUTE = "audio_mute"


class SensorName(default_collections.SensorName):
    BATOCERA_VERSION = "Batocera Version"
    AUDIO_VOLUME = "Audio Volume"
    AUDIO_MUTE = "Audio Mute"
