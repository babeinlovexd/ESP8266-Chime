import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import CONF_ID

from . import esp8266_chime_ns, Esp8266Chime

CONF_ESP8266_CHIME_ID = "esp8266_chime_id"

CONF_CHIME_VOLUME = "chime_volume"
CONF_CHIME_REPS = "chime_reps"
CONF_ALARM_VOLUME = "alarm_volume"

Esp8266ChimeVolumeNumber = esp8266_chime_ns.class_("Esp8266ChimeVolumeNumber", number.Number, cg.Component)
Esp8266ChimeRepsNumber = esp8266_chime_ns.class_("Esp8266ChimeRepsNumber", number.Number, cg.Component)
Esp8266AlarmVolumeNumber = esp8266_chime_ns.class_("Esp8266AlarmVolumeNumber", number.Number, cg.Component)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_ESP8266_CHIME_ID): cv.use_id(Esp8266Chime),
    cv.Optional(CONF_CHIME_VOLUME, default={"name": "Chime Lautstärke"}): number.number_schema(Esp8266ChimeVolumeNumber).extend(cv.COMPONENT_SCHEMA),
    cv.Optional(CONF_CHIME_REPS, default={"name": "Chime Wiederholungen"}): number.number_schema(Esp8266ChimeRepsNumber).extend(cv.COMPONENT_SCHEMA),
    cv.Optional(CONF_ALARM_VOLUME, default={"name": "Alarm Lautstärke"}): number.number_schema(Esp8266AlarmVolumeNumber).extend(cv.COMPONENT_SCHEMA),
})

async def to_code(config):
    hub = await cg.get_variable(config[CONF_ESP8266_CHIME_ID])

    conf = config[CONF_CHIME_VOLUME]
    var = cg.new_Pvariable(conf[CONF_ID])
    await cg.register_component(var, conf)
    await number.register_number(var, conf, min_value=0, max_value=100, step=1)
    cg.add(var.set_parent(hub))
    cg.add(hub.set_chime_volume_number(var))

    conf = config[CONF_CHIME_REPS]
    var = cg.new_Pvariable(conf[CONF_ID])
    await cg.register_component(var, conf)
    await number.register_number(var, conf, min_value=1, max_value=5, step=1)
    cg.add(var.set_parent(hub))
    cg.add(hub.set_chime_reps_number(var))

    conf = config[CONF_ALARM_VOLUME]
    var = cg.new_Pvariable(conf[CONF_ID])
    await cg.register_component(var, conf)
    await number.register_number(var, conf, min_value=0, max_value=100, step=1)
    cg.add(var.set_parent(hub))
    cg.add(hub.set_alarm_volume_number(var))
