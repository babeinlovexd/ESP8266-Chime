#pragma once

#include "esphome/core/component.h"
#include "esphome/components/number/number.h"
#include "esphome/components/select/select.h"
#include "esphome/components/button/button.h"
#include "esphome/core/hal.h"

#include <AudioFileSourcePROGMEM.h>
#include <AudioGeneratorWAV.h>
#include <AudioOutputI2S.h>

namespace esphome {
namespace esp8266_chime {

class Esp8266Chime : public Component {
 public:
  Esp8266Chime() {}

  void setup() override;
  void loop() override;

  void set_bclk_pin(InternalGPIOPin *pin) { this->bclk_pin_ = pin; }
  void set_ws_pin(InternalGPIOPin *pin) { this->ws_pin_ = pin; }
  void set_dout_pin(InternalGPIOPin *pin) { this->dout_pin_ = pin; }
  void set_sd_pin(GPIOPin *pin) { this->sd_pin_ = pin; }

  void set_volume_number(number::Number *num) { this->volume_number_ = num; }
  void set_sound_select(select::Select *sel) { this->sound_select_ = sel; }
  void set_play_button(button::Button *btn) { this->play_button_ = btn; }

  void play();
  void stop();
  void set_volume(float volume); // 0.0 to 1.0

 protected:
  InternalGPIOPin *bclk_pin_{nullptr};
  InternalGPIOPin *ws_pin_{nullptr};
  InternalGPIOPin *dout_pin_{nullptr};
  GPIOPin *sd_pin_{nullptr};

  number::Number *volume_number_{nullptr};
  select::Select *sound_select_{nullptr};
  button::Button *play_button_{nullptr};

  AudioFileSourcePROGMEM *in_{nullptr};
  AudioGeneratorWAV *wav_{nullptr};
  AudioOutputI2S *out_{nullptr};

  bool is_playing_{false};
  uint32_t play_start_time_{0};
  float current_volume_{1.0};
};

class Esp8266ChimeVolumeNumber : public number::Number, public Component {
 public:
  void set_parent(Esp8266Chime *parent) { this->parent_ = parent; }

 protected:
  void control(float value) override;
  Esp8266Chime *parent_{nullptr};
};

class Esp8266ChimeSoundSelect : public select::Select, public Component {
 public:
  void set_parent(Esp8266Chime *parent) { this->parent_ = parent; }

 protected:
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

}  // namespace esp8266_chime
}  // namespace esphome
