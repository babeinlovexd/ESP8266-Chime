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

CONF_CHIME_VOLUME = "chime_volume"
CONF_CHIME_REPS = "chime_reps"
CONF_ALARM_VOLUME = "alarm_volume"
CONF_CHIME_SOUND = "chime_sound"
CONF_ALARM_SOUND = "alarm_sound"
CONF_CHIME_PLAY = "chime_play"
CONF_ALARM_LOOP = "alarm_loop"

Esp8266ChimeVolumeNumber = esp8266_chime_ns.class_("Esp8266ChimeVolumeNumber", number.Number, cg.Component)
Esp8266ChimeRepsNumber = esp8266_chime_ns.class_("Esp8266ChimeRepsNumber", number.Number, cg.Component)
Esp8266AlarmVolumeNumber = esp8266_chime_ns.class_("Esp8266AlarmVolumeNumber", number.Number, cg.Component)

Esp8266ChimeSoundSelect = esp8266_chime_ns.class_("Esp8266ChimeSoundSelect", select.Select, cg.Component)
Esp8266AlarmSoundSelect = esp8266_chime_ns.class_("Esp8266AlarmSoundSelect", select.Select, cg.Component)

Esp8266ChimePlayButton = esp8266_chime_ns.class_("Esp8266ChimePlayButton", button.Button, cg.Component)

Esp8266AlarmLoopSwitch = esp8266_chime_ns.class_("Esp8266AlarmLoopSwitch", switch.Switch, cg.Component)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(Esp8266Chime),
        cv.Required(CONF_BCLK): pins.internal_gpio_output_pin_schema,
        cv.Required(CONF_WS): pins.internal_gpio_output_pin_schema,
        cv.Required(CONF_DOUT): pins.internal_gpio_output_pin_schema,
        cv.Required(CONF_SD): pins.gpio_output_pin_schema,

        cv.Optional(CONF_CHIME_VOLUME, default={"name": "Chime Lautstärke"}): number.number_schema(Esp8266ChimeVolumeNumber).extend(cv.COMPONENT_SCHEMA),
        cv.Optional(CONF_CHIME_REPS, default={"name": "Chime Wiederholungen"}): number.number_schema(Esp8266ChimeRepsNumber).extend(cv.COMPONENT_SCHEMA),
        cv.Optional(CONF_ALARM_VOLUME, default={"name": "Alarm Lautstärke"}): number.number_schema(Esp8266AlarmVolumeNumber).extend(cv.COMPONENT_SCHEMA),

        cv.Optional(CONF_CHIME_SOUND, default={"name": "Chime Ton"}): select.select_schema(Esp8266ChimeSoundSelect).extend(cv.COMPONENT_SCHEMA),
        cv.Optional(CONF_ALARM_SOUND, default={"name": "Alarm Ton"}): select.select_schema(Esp8266AlarmSoundSelect).extend(cv.COMPONENT_SCHEMA),

        cv.Optional(CONF_CHIME_PLAY, default={"name": "Chime Abspielen"}): button.button_schema(Esp8266ChimePlayButton).extend(cv.COMPONENT_SCHEMA),

        cv.Optional(CONF_ALARM_LOOP, default={"name": "Alarm Loop"}): switch.switch_schema(Esp8266AlarmLoopSwitch).extend(cv.COMPONENT_SCHEMA),
    }
).extend(cv.COMPONENT_SCHEMA)

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

    # Number Entities
    conf = config[CONF_CHIME_VOLUME]
    n_var = cg.new_Pvariable(conf[CONF_ID])
    await cg.register_component(n_var, conf)
    await number.register_number(n_var, conf, min_value=0, max_value=100, step=1)
    cg.add(n_var.set_parent(var))
    cg.add(var.set_chime_volume_number(n_var))

    conf = config[CONF_CHIME_REPS]
    n_var = cg.new_Pvariable(conf[CONF_ID])
    await cg.register_component(n_var, conf)
    await number.register_number(n_var, conf, min_value=1, max_value=5, step=1)
    cg.add(n_var.set_parent(var))
    cg.add(var.set_chime_reps_number(n_var))

    conf = config[CONF_ALARM_VOLUME]
    n_var = cg.new_Pvariable(conf[CONF_ID])
    await cg.register_component(n_var, conf)
    await number.register_number(n_var, conf, min_value=0, max_value=100, step=1)
    cg.add(n_var.set_parent(var))
    cg.add(var.set_alarm_volume_number(n_var))

    # Select Entities
    options = [
        "1. Ding Dong", "2. Trill Alarm", "3. Sweep Sound", "4. Solid Beep", "5. G5 Chime",
        "6. Siren", "7. Doorbell", "8. Notification", "9. Error", "10. Success",
        "11. Washing Machine", "12. Mail Delivered", "13. Window Open", "14. Pre Alarm", "15. Access Granted",
        "16. Notification Chime", "17. Notification Bloop", "18. Notification Pop", "19. Notification Sparkle", "20. Level Up",
        "21. Game Over", "22. Coin", "23. Notification Alert", "24. Glass Ping", "25. Elevator Ding",
        "26. Arcade Start", "27. Sci Fi Alert", "28. Soft Bell", "29. Magic Sparkle", "30. Bass Drop"
    ]

    conf = config[CONF_CHIME_SOUND]
    s_var = cg.new_Pvariable(conf[CONF_ID])
    await cg.register_component(s_var, conf)
    await select.register_select(s_var, conf, options=options)
    cg.add(s_var.set_parent(var))
    cg.add(var.set_chime_sound_select(s_var))

    conf = config[CONF_ALARM_SOUND]
    s_var = cg.new_Pvariable(conf[CONF_ID])
    await cg.register_component(s_var, conf)
    await select.register_select(s_var, conf, options=options)
    cg.add(s_var.set_parent(var))
    cg.add(var.set_alarm_sound_select(s_var))

    # Button Entity
    conf = config[CONF_CHIME_PLAY]
    b_var = cg.new_Pvariable(conf[CONF_ID])
    await cg.register_component(b_var, conf)
    await button.register_button(b_var, conf)
    cg.add(b_var.set_parent(var))
    cg.add(var.set_chime_play_button(b_var))

    # Switch Entity
    conf = config[CONF_ALARM_LOOP]
    sw_var = cg.new_Pvariable(conf[CONF_ID])
    await cg.register_component(sw_var, conf)
    await switch.register_switch(sw_var, conf)
    cg.add(sw_var.set_parent(var))
    cg.add(var.set_alarm_loop_switch(sw_var))
