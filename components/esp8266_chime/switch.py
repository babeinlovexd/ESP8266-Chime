import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ID

from . import esp8266_chime_ns, Esp8266Chime

CONF_ESP8266_CHIME_ID = "esp8266_chime_id"
CONF_ALARM_LOOP = "alarm_loop"

Esp8266AlarmLoopSwitch = esp8266_chime_ns.class_("Esp8266AlarmLoopSwitch", switch.Switch, cg.Component)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_ESP8266_CHIME_ID): cv.use_id(Esp8266Chime),
        cv.Optional(CONF_ALARM_LOOP, default={"name": "Alarm Loop"}): switch.switch_schema(Esp8266AlarmLoopSwitch).extend(cv.COMPONENT_SCHEMA),
    }
)

async def to_code(config):
    hub = await cg.get_variable(config[CONF_ESP8266_CHIME_ID])

    if CONF_ALARM_LOOP in config:
        conf = config[CONF_ALARM_LOOP]
        var = cg.new_Pvariable(conf[CONF_ID])
        await cg.register_component(var, conf)
        await switch.register_switch(var, conf)
        cg.add(var.set_parent(hub))
        cg.add(hub.set_alarm_loop_switch(var))
