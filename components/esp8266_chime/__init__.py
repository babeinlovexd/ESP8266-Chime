import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import number, select, button, switch
from esphome.const import CONF_ID

CODEOWNERS = ["@esphome"]
AUTO_LOAD = ["number", "select", "button", "switch"]

esp8266_chime_ns = cg.esphome_ns.namespace("esp8266_chime")
Esp8266Chime = esp8266_chime_ns.class_("Esp8266Chime", cg.Component)

CONF_BCLK = "bclk"
CONF_WS = "ws"
CONF_DOUT = "dout"
CONF_SD = "sd"

from . import number as esp8266_chime_number
from . import select as esp8266_chime_select
from . import button as esp8266_chime_button
from . import switch as esp8266_chime_switch

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(Esp8266Chime),
        cv.Required(CONF_BCLK): pins.internal_gpio_output_pin_schema,
        cv.Required(CONF_WS): pins.internal_gpio_output_pin_schema,
        cv.Required(CONF_DOUT): pins.internal_gpio_output_pin_schema,
        cv.Required(CONF_SD): pins.gpio_output_pin_schema,
    }
).extend(cv.COMPONENT_SCHEMA)

from .number import CONFIG_SCHEMA as NUMBER_SCHEMA
from .select import CONFIG_SCHEMA as SELECT_SCHEMA
from .button import CONFIG_SCHEMA as BUTTON_SCHEMA
from .switch import CONFIG_SCHEMA as SWITCH_SCHEMA

# Merge schemas from sub-components to allow them at the root component level
CONFIG_SCHEMA = CONFIG_SCHEMA.extend(NUMBER_SCHEMA)
CONFIG_SCHEMA = CONFIG_SCHEMA.extend(SELECT_SCHEMA)
CONFIG_SCHEMA = CONFIG_SCHEMA.extend(BUTTON_SCHEMA)
CONFIG_SCHEMA = CONFIG_SCHEMA.extend(SWITCH_SCHEMA)

MULTI_CONF = True

async def to_code(config):

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

    # We need to manually set esp8266_chime_id to point to var because we
    # merged the schemas and don't require the user to specify it.
    config_copy = dict(config)
    config_copy["esp8266_chime_id"] = config[CONF_ID]

    await esp8266_chime_number.to_code(config_copy)
    await esp8266_chime_select.to_code(config_copy)
    await esp8266_chime_button.to_code(config_copy)
    await esp8266_chime_switch.to_code(config_copy)
