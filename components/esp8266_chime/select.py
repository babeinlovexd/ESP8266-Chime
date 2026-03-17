import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import select
from esphome.const import CONF_ID

from . import esp8266_chime_ns, Esp8266Chime

CONF_ESP8266_CHIME_ID = "esp8266_chime_id"

CONF_CHIME_SOUND = "chime_sound"
CONF_ALARM_SOUND = "alarm_sound"

Esp8266ChimeSoundSelect = esp8266_chime_ns.class_("Esp8266ChimeSoundSelect", select.Select, cg.Component)
Esp8266AlarmSoundSelect = esp8266_chime_ns.class_("Esp8266AlarmSoundSelect", select.Select, cg.Component)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_ESP8266_CHIME_ID): cv.use_id(Esp8266Chime),
        cv.Optional(CONF_CHIME_SOUND, default={"name": "Chime Ton"}): select.select_schema(Esp8266ChimeSoundSelect).extend(cv.COMPONENT_SCHEMA),
        cv.Optional(CONF_ALARM_SOUND, default={"name": "Alarm Ton"}): select.select_schema(Esp8266AlarmSoundSelect).extend(cv.COMPONENT_SCHEMA),
    }
)

async def to_code(config):
    hub = await cg.get_variable(config[CONF_ESP8266_CHIME_ID])
    options = [
        "1. Ding Dong", "2. Trill Alarm", "3. Sweep Sound", "4. Solid Beep", "5. G5 Chime",
        "6. Siren", "7. Doorbell", "8. Notification", "9. Error", "10. Success"
    ]

    if CONF_CHIME_SOUND in config:
        conf = config[CONF_CHIME_SOUND]
        var = cg.new_Pvariable(conf[CONF_ID])
        await cg.register_component(var, conf)
        await select.register_select(var, conf, options=options)
        cg.add(var.set_parent(hub))
        cg.add(hub.set_chime_sound_select(var))

    if CONF_ALARM_SOUND in config:
        conf = config[CONF_ALARM_SOUND]
        var = cg.new_Pvariable(conf[CONF_ID])
        await cg.register_component(var, conf)
        await select.register_select(var, conf, options=options)
        cg.add(var.set_parent(hub))
        cg.add(hub.set_alarm_sound_select(var))
