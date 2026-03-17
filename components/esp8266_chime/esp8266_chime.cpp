#include "esp8266_chime.h"
#include "esphome/core/log.h"
#include "sounds.h"

namespace esphome {
namespace esp8266_chime {

static const char *const TAG = "esp8266_chime";

void Esp8266Chime::setup() {
  ESP_LOGCONFIG(TAG, "Setting up ESP8266 Chime...");

  if (this->sd_pin_ != nullptr) {
    this->sd_pin_->setup();
    this->sd_pin_->digital_write(true); // HIGH = mute LM4871
  }

  this->wav_ = new AudioGeneratorWAV();
  this->out_ = new AudioOutputI2S();

  // On ESP8266, I2S pins are fixed in hardware: BCLK=15, WS=2, DOUT=3
  // SetPinout is not supported/needed on this architecture.

  // Set default volume
  this->current_volume_ = 1.0;
  if (this->volume_number_ != nullptr) {
    this->volume_number_->publish_state(100.0);
  }

  if (this->sound_select_ != nullptr) {
      if (this->sound_select_->traits.get_options().size() > 0) {
          this->sound_select_->publish_state(this->sound_select_->traits.get_options()[0]);
      }
  }
}

void Esp8266Chime::loop() {
  if (this->is_playing_) {
    if (this->wav_ && this->wav_->isRunning()) {
      if (!this->wav_->loop()) {
        this->stop();
      }
    } else {
      this->stop();
    }
  }
}

void Esp8266Chime::play() {
  this->stop();

  if (this->sound_select_ == nullptr) {
    ESP_LOGW(TAG, "No sound selected");
    return;
  }

  std::string selected = this->sound_select_->state;
  const unsigned char *data = nullptr;
  unsigned int len = 0;

  if (selected == "1. Ding Dong") {
    data = sound_dingdong;
    len = sound_dingdong_len;
  } else if (selected == "2. Trill Alarm") {
    data = sound_trill;
    len = sound_trill_len;
  } else if (selected == "3. Sweep Sound") {
    data = sound_sweep;
    len = sound_sweep_len;
  } else if (selected == "4. Solid Beep") {
    data = sound_beep;
    len = sound_beep_len;
  } else if (selected == "5. G5 Chime") {
    data = sound_chime;
    len = sound_chime_len;
  } else {
    ESP_LOGE(TAG, "Unknown sound selected: %s", selected.c_str());
    return;
  }

  ESP_LOGD(TAG, "Playing sound: %s", selected.c_str());

  if (this->sd_pin_ != nullptr) {
    this->sd_pin_->digital_write(false); // LOW = enable amplifier
    delay(50); // 50ms delay
  }

  this->in_ = new AudioFileSourcePROGMEM(data, len);

  this->out_->SetGain(this->current_volume_);

  if (this->wav_->begin(this->in_, this->out_)) {
    this->is_playing_ = true;
  } else {
    ESP_LOGE(TAG, "Failed to begin WAV playback");
    this->stop();
  }
}

void Esp8266Chime::stop() {
  if (this->wav_ && this->wav_->isRunning()) {
    this->wav_->stop();
  }

  if (this->in_) {
    delete this->in_;
    this->in_ = nullptr;
  }

  if (this->sd_pin_ != nullptr) {
    this->sd_pin_->digital_write(true); // HIGH = mute amplifier
  }

  this->is_playing_ = false;
}

void Esp8266Chime::set_volume(float volume) {
  this->current_volume_ = volume;
  if (this->out_) {
    this->out_->SetGain(this->current_volume_);
  }
}

// ------------------------------------------

void Esp8266ChimeVolumeNumber::control(float value) {
  this->publish_state(value);
  if (this->parent_) {
    this->parent_->set_volume(value / 100.0f);
  }
}

void Esp8266ChimeSoundSelect::control(const std::string &value) {
  this->publish_state(value);
}

void Esp8266ChimePlayButton::press_action() {
  if (this->parent_) {
    this->parent_->play();
  }
}

}  // namespace esp8266_chime
}  // namespace esphome
