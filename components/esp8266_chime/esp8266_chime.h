#pragma once

#include "esphome/core/component.h"
#include "esphome/components/number/number.h"
#include "esphome/components/select/select.h"
#include "esphome/components/button/button.h"
#include "esphome/components/switch/switch.h"
#include "esphome/core/preferences.h"
#include "esphome/core/hal.h"

#ifdef USE_ESP8266
#include <core_esp8266_i2s.h>
#endif

namespace esphome {
namespace esp8266_chime {

enum class ChimeState {
  IDLE,
  PLAYING_CHIME,
  PLAYING_ALARM
};

class Esp8266Chime : public Component {
 public:
  Esp8266Chime() {}

  void setup() override;
  void loop() override;

  void set_bclk_pin(InternalGPIOPin *pin) { this->bclk_pin_ = pin; }
  void set_ws_pin(InternalGPIOPin *pin) { this->ws_pin_ = pin; }
  void set_dout_pin(InternalGPIOPin *pin) { this->dout_pin_ = pin; }
  void set_sd_pin(GPIOPin *pin) { this->sd_pin_ = pin; }

  void set_chime_volume_number(number::Number *num) { this->chime_volume_number_ = num; }
  void set_chime_reps_number(number::Number *num) { this->chime_reps_number_ = num; }
  void set_chime_sound_select(select::Select *sel) { this->chime_sound_select_ = sel; }
  void set_chime_play_button(button::Button *btn) { this->chime_play_button_ = btn; }

  void set_alarm_volume_number(number::Number *num) { this->alarm_volume_number_ = num; }
  void set_alarm_sound_select(select::Select *sel) { this->alarm_sound_select_ = sel; }
  void set_alarm_loop_switch(switch_::Switch *sw) { this->alarm_loop_switch_ = sw; }

  void play_chime();
  void play_alarm();
  void stop();
  void set_volume(float volume); // 0.0 to 1.0
  void handle_alarm_switch(bool state);

 protected:
  InternalGPIOPin *bclk_pin_{nullptr};
  InternalGPIOPin *ws_pin_{nullptr};
  InternalGPIOPin *dout_pin_{nullptr};
  GPIOPin *sd_pin_{nullptr};

  number::Number *chime_volume_number_{nullptr};
  number::Number *chime_reps_number_{nullptr};
  select::Select *chime_sound_select_{nullptr};
  button::Button *chime_play_button_{nullptr};

  number::Number *alarm_volume_number_{nullptr};
  select::Select *alarm_sound_select_{nullptr};
  switch_::Switch *alarm_loop_switch_{nullptr};

  ChimeState state_{ChimeState::IDLE};
  int current_rep_{0};
  int target_reps_{0};
  std::string current_sound_{""};
  float current_volume_{1.0};

  const unsigned char *current_data_{nullptr};
  unsigned int current_len_{0};
  unsigned int current_pos_{0};

  void play_internal(const std::string& sound_name);
};

class Esp8266ChimeVolumeNumber : public number::Number, public Component {
 public:
  void set_parent(Esp8266Chime *parent) { this->parent_ = parent; }

  void setup() override;
 protected:
  ESPPreferenceObject pref_;

  void control(float value) override;
  Esp8266Chime *parent_{nullptr};
};

class Esp8266ChimeRepsNumber : public number::Number, public Component {
 public:
  void set_parent(Esp8266Chime *parent) { this->parent_ = parent; }

  void setup() override;
 protected:
  ESPPreferenceObject pref_;

  void control(float value) override;
  Esp8266Chime *parent_{nullptr};
};

class Esp8266ChimeSoundSelect : public select::Select, public Component {
 public:
  void set_parent(Esp8266Chime *parent) { this->parent_ = parent; }

  void setup() override;
 protected:
  ESPPreferenceObject pref_;

  void control(const std::string &value) override;
  Esp8266Chime *parent_{nullptr};
};

class Esp8266ChimePlayButton : public button::Button, public Component {
 public:
  void set_parent(Esp8266Chime *parent) { this->parent_ = parent; }

 protected:
  void press_action() override;
  Esp8266Chime *parent_{nullptr};
};

class Esp8266AlarmVolumeNumber : public number::Number, public Component {
 public:
  void set_parent(Esp8266Chime *parent) { this->parent_ = parent; }

  void setup() override;
 protected:
  ESPPreferenceObject pref_;

  void control(float value) override;
  Esp8266Chime *parent_{nullptr};
};

class Esp8266AlarmSoundSelect : public select::Select, public Component {
 public:
  void set_parent(Esp8266Chime *parent) { this->parent_ = parent; }

  void setup() override;
 protected:
  ESPPreferenceObject pref_;

  void control(const std::string &value) override;
  Esp8266Chime *parent_{nullptr};
};

class Esp8266AlarmLoopSwitch : public switch_::Switch, public Component {
 public:
  void set_parent(Esp8266Chime *parent) { this->parent_ = parent; }

  void setup() override;
 protected:
  ESPPreferenceObject pref_;

  void write_state(bool state) override;
  Esp8266Chime *parent_{nullptr};
};

}  // namespace esp8266_chime
}  // namespace esphome
