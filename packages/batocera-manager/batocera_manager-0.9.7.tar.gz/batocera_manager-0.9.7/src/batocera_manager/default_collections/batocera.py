from ssh_terminal_manager import (
    ActionCommand,
    BinarySensor,
    Collection,
    Command,
    NumberSensor,
    SensorCommand,
    TextSensor,
    default_collections,
)

from .const import ActionKey, ActionName, SensorKey, SensorName

batocera = Collection(
    "Batocera",
    [
        *default_collections.linux.action_commands,
        ActionCommand(
            "/etc/init.d/S31emulationstation stop && /sbin/shutdown -h now",
            ActionName.TURN_OFF,
            ActionKey.TURN_OFF,
        ),
        ActionCommand(
            "/etc/init.d/S31emulationstation stop && /sbin/shutdown -r now",
            ActionName.RESTART,
            ActionKey.RESTART,
        ),
    ],
    [
        *default_collections.linux.sensor_commands,
        SensorCommand(
            "cat /userdata/system/data.version | awk '{print $1}'",
            sensors=[
                TextSensor(
                    SensorName.BATOCERA_VERSION,
                    SensorKey.BATOCERA_VERSION,
                )
            ],
        ),
        SensorCommand(
            'amixer -c0 get Master | awk -F"[][]" \'/dB/ {print $2+0;'
            + 'if($6=="on"){print "off"} if($6=="off"){print "on"}}\'',
            interval=15,
            sensors=[
                NumberSensor(
                    SensorName.AUDIO_VOLUME,
                    SensorKey.AUDIO_VOLUME,
                    unit="%",
                    command_set=Command("amixer -c0 set Master @{value}%"),
                ),
                BinarySensor(
                    SensorName.AUDIO_MUTE,
                    SensorKey.AUDIO_MUTE,
                    command_set=Command("amixer -c0 set Master toggle"),
                ),
            ],
        ),
    ],
)
