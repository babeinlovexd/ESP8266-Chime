#pragma once

#include "esphome.h"
#include <AudioFileSourcePROGMEM.h>
#include <AudioGeneratorWAV.h>
#include <AudioOutputI2S.h>

// 5 Dummy-PROGMEM-Arrays für WAV-Dateien (Ersetze die Werte durch echte WAV-Hex-Daten)
const uint8_t sound_1[] PROGMEM = { 0x52, 0x49, 0x46, 0x46 }; // Dummy RIFF Header
const uint8_t sound_2[] PROGMEM = { 0x52, 0x49, 0x46, 0x46 };
const uint8_t sound_3[] PROGMEM = { 0x52, 0x49, 0x46, 0x46 };
const uint8_t sound_4[] PROGMEM = { 0x52, 0x49, 0x46, 0x46 };
const uint8_t sound_5[] PROGMEM = { 0x52, 0x49, 0x46, 0x46 };

class ESP8266Chime : public esphome::Component {
protected:
  int shutdown_pin_;
  AudioGeneratorWAV *wav;
  AudioFileSourcePROGMEM *file;
  AudioOutputI2S *out;
  float volume_;

public:
  // Konstruktor mit Übergabe des Shutdown-Pins (GPIO12)
  ESP8266Chime(int shutdown_pin) {
    shutdown_pin_ = shutdown_pin;
    wav = new AudioGeneratorWAV();
    out = new AudioOutputI2S(); // Standard ESP8266 I2S Pins: BCLK=15, WS=2, DOUT=3
    file = nullptr;
    volume_ = 1.0;
  }

  void setup() override {
    pinMode(shutdown_pin_, OUTPUT);
    digitalWrite(shutdown_pin_, HIGH); // Mute-Pin HIGH = Amp initial stumm
    out->SetGain(volume_);
  }

  void play(int sound_id) {
    stop(); // Stoppt laufendes Audio und schaltet Amp stumm

    const uint8_t* sound_data = nullptr;
    uint32_t sound_len = 0;

    switch (sound_id) {
      case 1: sound_data = sound_1; sound_len = sizeof(sound_1); break;
      case 2: sound_data = sound_2; sound_len = sizeof(sound_2); break;
      case 3: sound_data = sound_3; sound_len = sizeof(sound_3); break;
      case 4: sound_data = sound_4; sound_len = sizeof(sound_4); break;
      case 5: sound_data = sound_5; sound_len = sizeof(sound_5); break;
      default: return; // Ungültige ID
    }

    // Amp einschalten (Shutdown = LOW)
    digitalWrite(shutdown_pin_, LOW);
    delay(50); // 50ms Pop-Schutz

    file = new AudioFileSourcePROGMEM(sound_data, sound_len);
    if (!wav->begin(file, out)) {
      // Wenn WAV-Datei ungültig, sofort stumm schalten
      stop();
    }
  }

  void stop() {
    if (wav->isRunning()) {
      wav->stop();
    }
    if (file != nullptr) {
      delete file;
      file = nullptr;
    }
    // Amp stumm (Shutdown = HIGH)
    digitalWrite(shutdown_pin_, HIGH);
  }

  void set_volume(float vol) {
    volume_ = vol;
    if (volume_ < 0.0f) volume_ = 0.0f;
    if (volume_ > 1.0f) volume_ = 1.0f;
    out->SetGain(volume_);
  }

  // Kritische Loop-Logik zum Füttern des Puffers
  void loop() override {
    if (wav->isRunning()) {
      if (!wav->loop()) {
        // Dateiende erreicht
        wav->stop();
        digitalWrite(shutdown_pin_, HIGH); // Automatisch stumm nach Dateiende, Rauschen verhindern
        if (file != nullptr) {
          delete file;
          file = nullptr;
        }
      }
    }
  }
};
