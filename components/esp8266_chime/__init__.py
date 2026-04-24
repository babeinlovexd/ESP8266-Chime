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
CONF_I2S_FORMAT = "i2s_format"

CONF_LED = "led"
CONF_OUT = "out"
CONF_FREQUENZ = "frequenz"
CONF_LED_DURATION = "duration"
CONF_LED_ACTIVATION = "activation"

CONF_CHIME_MUTE = "chime_mute"

CONF_CHIME_VOLUME = "chime_volume"
CONF_CHIME_REPS = "chime_reps"
CONF_ALARM_VOLUME = "alarm_volume"
CONF_CHIME_SOUND = "chime_sound"
CONF_ALARM_SOUND = "alarm_sound"
CONF_CHIME_PLAY = "chime_play"
CONF_ALARM_LOOP = "alarm_loop"

CONF_NOTIFY_VOLUME = "notify_volume"
CONF_NOTIFY_SOUND = "notify_sound"
CONF_NOTIFY_PLAY = "notify_play"


Esp8266ChimeVolumeNumber = esp8266_chime_ns.class_("Esp8266ChimeVolumeNumber", number.Number, cg.Component)
Esp8266ChimeRepsNumber = esp8266_chime_ns.class_("Esp8266ChimeRepsNumber", number.Number, cg.Component)
Esp8266AlarmVolumeNumber = esp8266_chime_ns.class_("Esp8266AlarmVolumeNumber", number.Number, cg.Component)

Esp8266ChimeSoundSelect = esp8266_chime_ns.class_("Esp8266ChimeSoundSelect", select.Select, cg.Component)
Esp8266AlarmSoundSelect = esp8266_chime_ns.class_("Esp8266AlarmSoundSelect", select.Select, cg.Component)

Esp8266ChimePlayButton = esp8266_chime_ns.class_("Esp8266ChimePlayButton", button.Button, cg.Component)

Esp8266AlarmLoopSwitch = esp8266_chime_ns.class_("Esp8266AlarmLoopSwitch", switch.Switch, cg.Component)

Esp8266NotifyVolumeNumber = esp8266_chime_ns.class_("Esp8266NotifyVolumeNumber", number.Number, cg.Component)
Esp8266NotifySoundSelect = esp8266_chime_ns.class_("Esp8266NotifySoundSelect", select.Select, cg.Component)
Esp8266NotifyPlayButton = esp8266_chime_ns.class_("Esp8266NotifyPlayButton", button.Button, cg.Component)


Esp8266LedDurationNumber = esp8266_chime_ns.class_("Esp8266LedDurationNumber", number.Number, cg.Component)
Esp8266LedEnableSwitch = esp8266_chime_ns.class_("Esp8266LedEnableSwitch", switch.Switch, cg.Component)
Esp8266ChimeMuteSwitch = esp8266_chime_ns.class_("Esp8266ChimeMuteSwitch", switch.Switch, cg.Component)

I2SFormat = esp8266_chime_ns.enum("I2SFormat")
I2S_FORMAT_OPTIONS = {
    "PHILIPS": I2SFormat.I2S_FORMAT_PHILIPS,
    "LSBJ": I2SFormat.I2S_FORMAT_LSBJ,
}

LEDFrequency = esp8266_chime_ns.enum("LEDFrequency")
LED_FREQUENZ_OPTIONS = {
    "low": LEDFrequency.LED_FREQ_LOW,
    "middle": LEDFrequency.LED_FREQ_MIDDLE,
    "high": LEDFrequency.LED_FREQ_HIGH,
}

LED_SCHEMA = cv.Schema({
    cv.Required(CONF_OUT): pins.gpio_output_pin_schema,
    cv.Optional(CONF_FREQUENZ, default="low"): cv.enum(LED_FREQUENZ_OPTIONS, lower=True),
    cv.Optional(CONF_LED_DURATION, default={"name": "LED Blinkdauer"}): number.number_schema(Esp8266LedDurationNumber).extend(cv.COMPONENT_SCHEMA),
    cv.Optional(CONF_LED_ACTIVATION, default={"name": "LED Aktivieren"}): switch.switch_schema(Esp8266LedEnableSwitch).extend(cv.COMPONENT_SCHEMA),
})

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(Esp8266Chime),
        cv.Required(CONF_BCLK): pins.internal_gpio_output_pin_schema,
        cv.Required(CONF_WS): pins.internal_gpio_output_pin_schema,
        cv.Required(CONF_DOUT): pins.internal_gpio_output_pin_schema,
        cv.Required(CONF_SD): pins.gpio_output_pin_schema,
        cv.Optional(CONF_I2S_FORMAT, default="PHILIPS"): cv.enum(I2S_FORMAT_OPTIONS, upper=True),

        cv.Optional(CONF_CHIME_VOLUME, default={"name": "Chime Lautstärke"}): number.number_schema(Esp8266ChimeVolumeNumber).extend(cv.COMPONENT_SCHEMA),
        cv.Optional(CONF_CHIME_REPS, default={"name": "Chime Wiederholungen"}): number.number_schema(Esp8266ChimeRepsNumber).extend(cv.COMPONENT_SCHEMA),
        cv.Optional(CONF_ALARM_VOLUME, default={"name": "Alarm Lautstärke"}): number.number_schema(Esp8266AlarmVolumeNumber).extend(cv.COMPONENT_SCHEMA),

        cv.Optional(CONF_CHIME_SOUND, default={"name": "Chime Ton"}): select.select_schema(Esp8266ChimeSoundSelect).extend(cv.COMPONENT_SCHEMA),
        cv.Optional(CONF_ALARM_SOUND, default={"name": "Alarm Ton"}): select.select_schema(Esp8266AlarmSoundSelect).extend(cv.COMPONENT_SCHEMA),

        cv.Optional(CONF_CHIME_PLAY, default={"name": "Chime Abspielen"}): button.button_schema(Esp8266ChimePlayButton).extend(cv.COMPONENT_SCHEMA),

        cv.Optional(CONF_CHIME_MUTE, default={"name": "Chime Mute"}): switch.switch_schema(Esp8266ChimeMuteSwitch).extend(cv.COMPONENT_SCHEMA),

        cv.Optional(CONF_ALARM_LOOP, default={"name": "Alarm Loop"}): switch.switch_schema(Esp8266AlarmLoopSwitch).extend(cv.COMPONENT_SCHEMA),

        cv.Optional(CONF_NOTIFY_VOLUME, default={"name": "Notify Lautstärke"}): number.number_schema(Esp8266NotifyVolumeNumber).extend(cv.COMPONENT_SCHEMA),
        cv.Optional(CONF_NOTIFY_SOUND, default={"name": "Notify Ton"}): select.select_schema(Esp8266NotifySoundSelect).extend(cv.COMPONENT_SCHEMA),
        cv.Optional(CONF_NOTIFY_PLAY, default={"name": "Notify Abspielen"}): button.button_schema(Esp8266NotifyPlayButton).extend(cv.COMPONENT_SCHEMA),


        cv.Optional(CONF_LED): LED_SCHEMA,
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

    cg.add(var.set_i2s_format(config[CONF_I2S_FORMAT]))

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
        "26. Arcade Start", "27. Sci Fi Alert", "28. Soft Bell", "29. Magic Sparkle", "30. Bass Drop",

        "TTS: Essen ist Fertig", "TTS: Waschmaschine ist fertig", "TTS: Trockner ist fertig",
        "TTS: Post ist da", "TTS: Bitte runter kommen", "TTS: Schwarze Mülltonne muss raus",
        "TTS: Grüne Mülltonne muss raus", "TTS: Gelbe Mülltonne muss raus", "TTS: Glas muss raus",
        "TTS: Zähne putzen"
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


    conf = config[CONF_NOTIFY_VOLUME]
    n_var = cg.new_Pvariable(conf[CONF_ID])
    await cg.register_component(n_var, conf)
    await number.register_number(n_var, conf, min_value=0, max_value=100, step=1)
    cg.add(n_var.set_parent(var))
    cg.add(var.set_notify_volume_number(n_var))

    conf = config[CONF_NOTIFY_SOUND]
    s_var = cg.new_Pvariable(conf[CONF_ID])
    await cg.register_component(s_var, conf)
    await select.register_select(s_var, conf, options=options)
    cg.add(s_var.set_parent(var))
    cg.add(var.set_notify_sound_select(s_var))

    conf = config[CONF_NOTIFY_PLAY]
    b_var = cg.new_Pvariable(conf[CONF_ID])
    await cg.register_component(b_var, conf)
    await button.register_button(b_var, conf)
    cg.add(b_var.set_parent(var))
    cg.add(var.set_notify_play_button(b_var))

    # Switch Entities
    conf = config[CONF_ALARM_LOOP]
    sw_var = cg.new_Pvariable(conf[CONF_ID])
    await cg.register_component(sw_var, conf)
    await switch.register_switch(sw_var, conf)
    cg.add(sw_var.set_parent(var))
    cg.add(var.set_alarm_loop_switch(sw_var))

    conf = config[CONF_CHIME_MUTE]
    sw_var = cg.new_Pvariable(conf[CONF_ID])
    await cg.register_component(sw_var, conf)
    await switch.register_switch(sw_var, conf)
    cg.add(sw_var.set_parent(var))
    cg.add(var.set_chime_mute_switch(sw_var))

    if CONF_LED in config:
        led_config = config[CONF_LED]
        led_pin = await cg.gpio_pin_expression(led_config[CONF_OUT])
        cg.add(var.set_led_pin(led_pin))
        cg.add(var.set_led_frequenz(led_config[CONF_FREQUENZ]))

        # Blinkdauer Slider (1-15s)
        conf = led_config[CONF_LED_DURATION]
        dn_var = cg.new_Pvariable(conf[CONF_ID])
        await cg.register_component(dn_var, conf)
        await number.register_number(dn_var, conf, min_value=1, max_value=15, step=1)
        cg.add(dn_var.set_parent(var))
        cg.add(var.set_led_duration_number(dn_var))

        # LED On/Off Switch
        conf = led_config[CONF_LED_ACTIVATION]
        ls_var = cg.new_Pvariable(conf[CONF_ID])
        await cg.register_component(ls_var, conf)
        await switch.register_switch(ls_var, conf)
        cg.add(ls_var.set_parent(var))
        cg.add(var.set_led_enable_switch(ls_var))
