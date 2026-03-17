import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import select
from esphome.const import CONF_ID

from . import esp8266_chime_ns, Esp8266Chime

CONF_ESP8266_CHIME_ID = "esp8266_chime_id"

Esp8266ChimeSoundSelect = esp8266_chime_ns.class_("Esp8266ChimeSoundSelect", select.Select)

CONFIG_SCHEMA = select.select_schema(Esp8266ChimeSoundSelect).extend(
    {
        cv.GenerateID(CONF_ESP8266_CHIME_ID): cv.use_id(Esp8266Chime),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await select.register_select(var, config, options=["1. Ding Dong", "2. Trill Alarm", "3. Sweep Sound", "4. Solid Beep", "5. G5 Chime"])

    hub = config[CONF_ESP8266_CHIME_ID]
    cg.add(var.set_parent(hub))
    cg.add(hub.set_sound_select(var))
