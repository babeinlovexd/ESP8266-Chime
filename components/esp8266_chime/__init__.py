import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import number, select, button
from esphome.const import CONF_ID

CODEOWNERS = ["@esphome"]
DEPENDENCIES = []

esp8266_chime_ns = cg.esphome_ns.namespace("esp8266_chime")
Esp8266Chime = esp8266_chime_ns.class_("Esp8266Chime", cg.Component)

CONF_BCLK = "bclk"
CONF_WS = "ws"
CONF_DOUT = "dout"
CONF_SD = "sd"

from esphome.const import CONF_VOLUME, CONF_MODE

CONF_PLAY_BUTTON = "play_button"

from . import number as esp8266_chime_number
from . import select as esp8266_chime_select
from . import button as esp8266_chime_button

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(Esp8266Chime),
        cv.Required(CONF_BCLK): pins.internal_gpio_output_pin_schema,
        cv.Required(CONF_WS): pins.internal_gpio_output_pin_schema,
        cv.Required(CONF_DOUT): pins.internal_gpio_output_pin_schema,
        cv.Required(CONF_SD): pins.gpio_output_pin_schema,
        cv.Optional(CONF_VOLUME, default={"name": "Chime Volume"}): esp8266_chime_number.CONFIG_SCHEMA,
        cv.Optional(CONF_MODE, default={"name": "Chime Sound"}): esp8266_chime_select.CONFIG_SCHEMA,
        cv.Optional(CONF_PLAY_BUTTON, default={"name": "Chime Play"}): esp8266_chime_button.CONFIG_SCHEMA,
    }
).extend(cv.COMPONENT_SCHEMA)


MULTI_CONF = True

async def to_code(config):
    cg.add_library("earlephilhower/ESP8266Audio", "1.9.7")

    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    bclk_pin = await cg.gpio_pin_expression(config[CONF_BCLK])
    cg.add(var.set_bclk_pin(bclk_pin))

    ws_pin = await cg.gpio_pin_expression(config[CONF_WS])
    cg.add(var.set_ws_pin(ws_pin))

    dout_pin = await cg.gpio_pin_expression(config[CONF_DOUT])
    cg.add(var.set_dout_pin(dout_pin))

    sd_pin = await cg.gpio_pin_expression(config[CONF_SD])
    cg.add(var.set_sd_pin(sd_pin))

    if CONF_VOLUME in config:
        conf = config[CONF_VOLUME]
        conf[esp8266_chime_number.CONF_ESP8266_CHIME_ID] = var
        await esp8266_chime_number.to_code(conf)

    if CONF_MODE in config:
        conf = config[CONF_MODE]
        conf[esp8266_chime_select.CONF_ESP8266_CHIME_ID] = var
        await esp8266_chime_select.to_code(conf)

    if CONF_PLAY_BUTTON in config:
        conf = config[CONF_PLAY_BUTTON]
        conf[esp8266_chime_button.CONF_ESP8266_CHIME_ID] = var
        await esp8266_chime_button.to_code(conf)
