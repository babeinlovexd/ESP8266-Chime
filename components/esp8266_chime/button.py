import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import button
from esphome.const import CONF_ID

from . import esp8266_chime_ns, Esp8266Chime

CONF_ESP8266_CHIME_ID = "esp8266_chime_id"

CONF_CHIME_PLAY = "chime_play"

Esp8266ChimePlayButton = esp8266_chime_ns.class_("Esp8266ChimePlayButton", button.Button, cg.Component)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_ESP8266_CHIME_ID): cv.use_id(Esp8266Chime),
        cv.Optional(CONF_CHIME_PLAY, default={"name": "Chime Abspielen"}): button.button_schema(Esp8266ChimePlayButton).extend(cv.COMPONENT_SCHEMA),
    }
)

async def to_code(config):
    hub = await cg.get_variable(config[CONF_ESP8266_CHIME_ID])

    conf = config.get(CONF_CHIME_PLAY, {})
    if not conf:
        conf = {"name": "Chime Abspielen"}
        conf[CONF_ID] = cg.ObjectID("chime_play_button", type=Esp8266ChimePlayButton)

    var = cg.new_Pvariable(conf[CONF_ID])
    await cg.register_component(var, conf)
    await button.register_button(var, conf)
    cg.add(var.set_parent(hub))
    cg.add(hub.set_chime_play_button(var))
