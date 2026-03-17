import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import button
from esphome.const import CONF_ID

from . import esp8266_chime_ns, Esp8266Chime

CONF_ESP8266_CHIME_ID = "esp8266_chime_id"

Esp8266ChimePlayButton = esp8266_chime_ns.class_("Esp8266ChimePlayButton", button.Button)

CONFIG_SCHEMA = button.button_schema(Esp8266ChimePlayButton).extend(
    {
        cv.GenerateID(CONF_ESP8266_CHIME_ID): cv.use_id(Esp8266Chime),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await button.register_button(var, config)

    hub = config[CONF_ESP8266_CHIME_ID]
    cg.add(var.set_parent(hub))
    cg.add(hub.set_play_button(var))
