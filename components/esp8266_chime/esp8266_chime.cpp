#include "esp8266_chime.h"
#include "esphome/core/log.h"
#include "sounds.h"
#include <Arduino.h>
#include <i2s_reg.h>

namespace esphome {
namespace esp8266_chime {

static const char *const TAG = "esp8266_chime";

void Esp8266Chime::setup() {
  ESP_LOGCONFIG(TAG, "Setting up ESP8266 Chime...");

  if (this->sd_pin_ != nullptr) {
    this->sd_pin_->setup();
    this->sd_pin_->digital_write(true); // HIGH = mute LM4871
  }

#ifdef USE_ESP8266
  i2s_begin();
  i2s_set_rate(8000);

  if (this->i2s_format_ == I2S_FORMAT_LSBJ) {
    // Fix for PT8211 (Japanese Format LSBJ)
    // Clears the I2S_TX_MSB_SHIFT bit to disable the default Philips format
    I2SC &= ~(1 << 15);
  }
#endif
}

void Esp8266Chime::loop() {
#ifdef USE_ESP8266
  if (this->state_ == ChimeState::PLAYING_CHIME || this->state_ == ChimeState::PLAYING_ALARM) {
    if (this->current_data_ != nullptr && this->current_pos_ < this->current_len_) {
      // Feed I2S FIFO as much as possible without blocking
      while (this->current_pos_ < this->current_len_) {
        // Read 16-bit sample from PROGMEM
        int16_t sample = (int16_t)(
            pgm_read_byte(&this->current_data_[this->current_pos_]) |
            (pgm_read_byte(&this->current_data_[this->current_pos_ + 1]) << 8)
        );

        // Apply volume
        sample = (int16_t)(sample * this->current_volume_);

        // The DAC PT8211 needs stereo data, so we combine L and R into one 32-bit sample
        // Left channel in lower 16 bits, Right channel in upper 16 bits.
        uint32_t stereo_sample = ((uint32_t)(uint16_t)sample << 16) | (uint16_t)sample;
        // ESP8266 i2s_write_sample_nb returns true if it fits in the buffer
        if (i2s_write_sample_nb(stereo_sample)) {
            this->current_pos_ += 2;
        } else {
            // Buffer full, come back next loop
            break;
        }
      }

      if (this->current_pos_ >= this->current_len_) {
        // Sound finished
        if (this->state_ == ChimeState::PLAYING_CHIME) {
          this->current_rep_++;
          if (this->current_rep_ < this->target_reps_) {
            // Replay
            this->play_internal(this->current_sound_);
          } else {
            // Done
            this->stop();
          }
        } else if (this->state_ == ChimeState::PLAYING_ALARM) {
          // Alarm loops endlessly until switch is toggled off
          this->play_internal(this->current_sound_);
        }
      }
    }
  }
#endif
}

void Esp8266Chime::play_chime() {
  if (this->state_ == ChimeState::PLAYING_ALARM) {
    ESP_LOGI(TAG, "Alarm is active. Chime request ignored.");
    return;
  }

  this->stop();

  if (this->chime_sound_select_ == nullptr || this->chime_reps_number_ == nullptr || this->chime_volume_number_ == nullptr) {
    ESP_LOGW(TAG, "Chime components not fully configured");
    return;
  }

  this->target_reps_ = (int)this->chime_reps_number_->state;
  this->current_rep_ = 0;

  if (this->chime_sound_select_->has_state()) {
      this->current_sound_ = this->chime_sound_select_->current_option();
  } else {
      this->current_sound_ = this->chime_sound_select_->traits.get_options()[0];
  }

  this->set_volume(this->chime_volume_number_->state / 100.0f);
  this->state_ = ChimeState::PLAYING_CHIME;

  this->play_internal(this->current_sound_);
}

void Esp8266Chime::play_alarm() {
  this->stop();

  if (this->alarm_sound_select_ == nullptr || this->alarm_volume_number_ == nullptr) {
    ESP_LOGW(TAG, "Alarm components not fully configured");
    return;
  }

  if (this->alarm_sound_select_->has_state()) {
      this->current_sound_ = this->alarm_sound_select_->current_option();
  } else {
      this->current_sound_ = this->alarm_sound_select_->traits.get_options()[0];
  }

  this->set_volume(this->alarm_volume_number_->state / 100.0f);
  this->state_ = ChimeState::PLAYING_ALARM;

  this->play_internal(this->current_sound_);
}

void Esp8266Chime::play_internal(const std::string& selected) {
  this->current_data_ = nullptr;
  this->current_len_ = 0;
  this->current_pos_ = 0;

  if (selected == "1. Ding Dong") {
    this->current_data_ = sound_dingdong;
    this->current_len_ = sound_dingdong_len;
  } else if (selected == "2. Trill Alarm") {
    this->current_data_ = sound_trill;
    this->current_len_ = sound_trill_len;
  } else if (selected == "3. Sweep Sound") {
    this->current_data_ = sound_sweep;
    this->current_len_ = sound_sweep_len;
  } else if (selected == "4. Solid Beep") {
    this->current_data_ = sound_beep;
    this->current_len_ = sound_beep_len;
  } else if (selected == "5. G5 Chime") {
    this->current_data_ = sound_chime;
    this->current_len_ = sound_chime_len;
  } else if (selected == "6. Siren") {
    this->current_data_ = sound_siren;
    this->current_len_ = sound_siren_len;
  } else if (selected == "7. Doorbell") {
    this->current_data_ = sound_doorbell;
    this->current_len_ = sound_doorbell_len;
  } else if (selected == "8. Notification") {
    this->current_data_ = sound_notification;
    this->current_len_ = sound_notification_len;
  } else if (selected == "9. Error") {
    this->current_data_ = sound_error;
    this->current_len_ = sound_error_len;
  } else if (selected == "10. Success") {
    this->current_data_ = sound_success;
    this->current_len_ = sound_success_len;
  } else if (selected == "11. Washing Machine") {
    this->current_data_ = sound_washing_machine;
    this->current_len_ = sound_washing_machine_len;
  } else if (selected == "12. Mail Delivered") {
    this->current_data_ = sound_mail_delivered;
    this->current_len_ = sound_mail_delivered_len;
  } else if (selected == "13. Window Open") {
    this->current_data_ = sound_window_open;
    this->current_len_ = sound_window_open_len;
  } else if (selected == "14. Pre Alarm") {
    this->current_data_ = sound_pre_alarm;
    this->current_len_ = sound_pre_alarm_len;
  } else if (selected == "15. Access Granted") {
    this->current_data_ = sound_access_granted;
    this->current_len_ = sound_access_granted_len;
  } else if (selected == "16. Notification Chime") {
    this->current_data_ = sound_noti_chime;
    this->current_len_ = sound_noti_chime_len;
  } else if (selected == "17. Notification Bloop") {
    this->current_data_ = sound_noti_bloop;
    this->current_len_ = sound_noti_bloop_len;
  } else if (selected == "18. Notification Pop") {
    this->current_data_ = sound_noti_pop;
    this->current_len_ = sound_noti_pop_len;
  } else if (selected == "19. Notification Sparkle") {
    this->current_data_ = sound_noti_sparkle;
    this->current_len_ = sound_noti_sparkle_len;
  } else if (selected == "20. Level Up") {
    this->current_data_ = sound_level_up;
    this->current_len_ = sound_level_up_len;
  } else if (selected == "21. Game Over") {
    this->current_data_ = sound_game_over;
    this->current_len_ = sound_game_over_len;
  } else if (selected == "22. Coin") {
    this->current_data_ = sound_coin;
    this->current_len_ = sound_coin_len;
  } else if (selected == "23. Notification Alert") {
    this->current_data_ = sound_noti_alert;
    this->current_len_ = sound_noti_alert_len;
  } else if (selected == "24. Glass Ping") {
    this->current_data_ = sound_glass_ping;
    this->current_len_ = sound_glass_ping_len;
  } else if (selected == "25. Elevator Ding") {
    this->current_data_ = sound_elevator_ding;
    this->current_len_ = sound_elevator_ding_len;
  } else if (selected == "26. Arcade Start") {
    this->current_data_ = sound_arcade_start;
    this->current_len_ = sound_arcade_start_len;
  } else if (selected == "27. Sci Fi Alert") {
    this->current_data_ = sound_sci_fi_alert;
    this->current_len_ = sound_sci_fi_alert_len;
  } else if (selected == "28. Soft Bell") {
    this->current_data_ = sound_soft_bell;
    this->current_len_ = sound_soft_bell_len;
  } else if (selected == "29. Magic Sparkle") {
    this->current_data_ = sound_magic_sparkle;
    this->current_len_ = sound_magic_sparkle_len;
  } else if (selected == "30. Bass Drop") {
    this->current_data_ = sound_bass_drop;
    this->current_len_ = sound_bass_drop_len;
  } else {
    ESP_LOGE(TAG, "Unknown sound selected: %s", selected.c_str());
    this->state_ = ChimeState::IDLE;
    return;
  }

  // Skip the standard 44 byte WAV header assuming 16-bit Mono 8000Hz PCM
  if (this->current_len_ > 44) {
      this->current_pos_ = 44;
  }

  ESP_LOGD(TAG, "Playing sound: %s", selected.c_str());

  if (this->sd_pin_ != nullptr) {
    this->sd_pin_->digital_write(false); // LOW = enable amplifier
    // Only delay if we are just starting from IDLE/stop, otherwise it might click between loops.
    // However, 50ms delay pop protection is requested.
    delay(50); // 50ms delay
  }
}

void Esp8266Chime::handle_alarm_switch(bool state) {
  if (state) {
    this->play_alarm();
  } else {
    this->stop();
  }
}

void Esp8266Chime::stop() {
  this->current_data_ = nullptr;
  this->current_len_ = 0;
  this->current_pos_ = 0;

  if (this->sd_pin_ != nullptr) {
    this->sd_pin_->digital_write(true); // HIGH = mute amplifier
  }

  this->state_ = ChimeState::IDLE;
}

void Esp8266Chime::set_volume(float volume) {
  this->current_volume_ = volume;
}


// ------------------------------------------

void Esp8266ChimeVolumeNumber::setup() {
  float value;
  this->pref_ = global_preferences->make_preference<float>(this->get_object_id_hash());
  if (this->pref_.load(&value)) {
    this->publish_state(value);
  } else {
    this->publish_state(100.0);
  }
}

void Esp8266ChimeVolumeNumber::control(float value) {
  this->publish_state(value);
  this->pref_.save(&value);
}

void Esp8266ChimeRepsNumber::setup() {
  float value;
  this->pref_ = global_preferences->make_preference<float>(this->get_object_id_hash());
  if (this->pref_.load(&value)) {
    this->publish_state(value);
  } else {
    this->publish_state(1.0);
  }
}

void Esp8266ChimeRepsNumber::control(float value) {
  this->publish_state(value);
  this->pref_.save(&value);
}

void Esp8266ChimeSoundSelect::setup() {
  size_t index;
  this->pref_ = global_preferences->make_preference<size_t>(this->get_object_id_hash());
  if (this->pref_.load(&index) && index < this->traits.get_options().size()) {
    this->publish_state(this->traits.get_options()[index]);
  } else if (this->traits.get_options().size() > 0) {
    this->publish_state(this->traits.get_options()[0]);
  }
}

void Esp8266ChimeSoundSelect::control(const std::string &value) {
  this->publish_state(value);
  const auto &options = this->traits.get_options();
  auto it = std::find(options.begin(), options.end(), value);
  if (it != options.end()) {
    size_t index = std::distance(options.begin(), it);
    this->pref_.save(&index);
  }
}

void Esp8266ChimePlayButton::press_action() {
  if (this->parent_) {
    this->parent_->play_chime();
  }
}

void Esp8266AlarmVolumeNumber::setup() {
  float value;
  this->pref_ = global_preferences->make_preference<float>(this->get_object_id_hash());
  if (this->pref_.load(&value)) {
    this->publish_state(value);
  } else {
    this->publish_state(100.0);
  }
}

void Esp8266AlarmVolumeNumber::control(float value) {
  this->publish_state(value);
  this->pref_.save(&value);
}

void Esp8266AlarmSoundSelect::setup() {
  size_t index;
  this->pref_ = global_preferences->make_preference<size_t>(this->get_object_id_hash());
  if (this->pref_.load(&index) && index < this->traits.get_options().size()) {
    this->publish_state(this->traits.get_options()[index]);
  } else if (this->traits.get_options().size() > 0) {
    this->publish_state(this->traits.get_options()[0]);
  }
}

void Esp8266AlarmSoundSelect::control(const std::string &value) {
  this->publish_state(value);
  const auto &options = this->traits.get_options();
  auto it = std::find(options.begin(), options.end(), value);
  if (it != options.end()) {
    size_t index = std::distance(options.begin(), it);
    this->pref_.save(&index);
  }
}

void Esp8266AlarmLoopSwitch::setup() {
  bool state;
  this->pref_ = global_preferences->make_preference<bool>(this->get_object_id_hash());
  if (this->pref_.load(&state)) {
    this->publish_state(state);
    if (this->parent_) {
      this->parent_->handle_alarm_switch(state);
    }
  } else {
    this->publish_state(false);
  }
}

void Esp8266AlarmLoopSwitch::write_state(bool state) {
  this->publish_state(state);
  this->pref_.save(&state);
  if (this->parent_) {
    this->parent_->handle_alarm_switch(state);
  }
}

}  // namespace esp8266_chime
}  // namespace esphome
