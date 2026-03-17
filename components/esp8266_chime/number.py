import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import CONF_ID

from . import esp8266_chime_ns, Esp8266Chime

CONF_ESP8266_CHIME_ID = "esp8266_chime_id"

Esp8266ChimeVolumeNumber = esp8266_chime_ns.class_("Esp8266ChimeVolumeNumber", number.Number)

CONFIG_SCHEMA = number.NUMBER_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(Esp8266ChimeVolumeNumber),
        cv.GenerateID(CONF_ESP8266_CHIME_ID): cv.use_id(Esp8266Chime),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await number.register_number(var, config, min_value=0, max_value=100, step=1)

    hub = config[CONF_ESP8266_CHIME_ID]
    cg.add(var.set_parent(hub))
    cg.add(hub.set_volume_number(var))
