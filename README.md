# ESP8266-Chime für ESPHome

Eine maßgeschneiderte (Custom) ESPHome-Komponente für den ESP8266 (z.B. Wemos D1 Mini), um autark WAV-Dateien aus dem Flash-Speicher (PROGMEM) über I2S abzuspielen.

## Hardware-Setup

*   **MCU:** ESP8266 (z.B. Wemos D1 Mini)
*   **DAC:** PT8211 (I2S Hardware DAC)
*   **Verstärker:** LM4871 (Audio Amp mit Shutdown-Pin)

### Pin-Belegung

| ESP8266 Pin | Funktion | Verbunden mit |
| :--- | :--- | :--- |
| GPIO15 (D8) | I2S BCLK | PT8211 BCK |
| GPIO2 (D4) | I2S WS (Word Select) | PT8211 WS |
| GPIO3 (RX) | I2S DIN / DOUT | PT8211 DIN |
| GPIO12 (D6) | Amp Shutdown | LM4871 Shutdown Pin |

> **Wichtig:** Da GPIO3 (RX) für die I2S-Datenübertragung genutzt wird, **muss** im ESPHome-YAML die `baud_rate: 0` für den Logger gesetzt werden. Andernfalls blockiert die serielle Ausgabe die Audioausgabe.

## Einbindung eigener WAV-Dateien

Das Projekt ist darauf ausgelegt, 5 WAV-Dateien direkt im Flash-Speicher (PROGMEM) des ESP8266 zu hinterlegen.

1.  **Audiodateien vorbereiten:** Die WAV-Dateien sollten mono, 8-bit oder 16-bit sein und eine passende Samplerate (z.B. 16kHz oder 22.05kHz) haben, um Platz zu sparen.
2.  **Konvertierung in C-Arrays:** Nutze ein Tool wie `xxd` (unter Linux/macOS oft vorinstalliert, für Windows via Git Bash oder WSL verfügbar), um die `.wav` Dateien in Hex-Werte umzuwandeln.

    ```bash
    xxd -i mein_sound.wav > mein_sound.h
    ```
    Das Ergebnis sieht in etwa so aus:
    ```c
    unsigned char mein_sound_wav[] = {
      0x52, 0x49, 0x46, 0x46, 0x24, 0x08, 0x00, 0x00, 0x57, 0x41, 0x56, 0x45,
      // ... viele weitere Zeilen ...
    };
    unsigned int mein_sound_wav_len = 2084;
    ```
3.  **In `ESP8266-Chime.h` einfügen:** Ersetze die Dummy-Arrays (`sound_1` bis `sound_5`) in der Datei `ESP8266-Chime.h` durch die mit `xxd` generierten Hex-Daten.

## Home Assistant Integration & Beispiele

Nachdem die Firmware via ESPHome auf den ESP8266 geflasht wurde, stehen in Home Assistant drei neue Services (Dienste) zur Verfügung:

1.  `esphome.esp8266_chime_play_sound`
2.  `esphome.esp8266_chime_stop_sound`
3.  `esphome.esp8266_chime_set_volume`

*(Hinweis: Der genaue Service-Name in Home Assistant hängt vom Namen deines ESPHome-Geräts ab. Wenn dein Gerät `esp8266-chime` heißt, beginnen die Services mit `esphome.esp8266_chime_...`)*

### Beispiel 1: Sound abspielen (Automation)

Spielt Sound Nr. 1 ab, wenn eine Türklingel gedrückt wird.

```yaml
alias: "Klingel: Sound 1 abspielen"
trigger:
  - platform: state
    entity_id: binary_sensor.tuerklingel
    to: "on"
action:
  - service: esphome.esp8266_chime_play_sound
    data:
      sound_id: 1
```

### Beispiel 2: Lautstärke setzen und Sound abspielen (Skript)

Dieses Skript setzt die Lautstärke auf 50% (0.5) und spielt dann Sound Nr. 3 ab.

```yaml
alias: "Chime: Warnung abspielen"
sequence:
  - service: esphome.esp8266_chime_set_volume
    data:
      volume: 0.5
  - service: esphome.esp8266_chime_play_sound
    data:
      sound_id: 3
```

### Beispiel 3: Wiedergabe sofort stoppen

Bricht die aktuelle Wiedergabe sofort ab. Der Verstärker wird automatisch wieder stummgeschaltet.

```yaml
alias: "Chime: Stumm schalten"
sequence:
  - service: esphome.esp8266_chime_stop_sound
```

## Besonderheiten der Implementierung

*   **Pop-Schutz:** Bevor eine Audiodatei gestartet wird, wird der Verstärker eingeschaltet (Shutdown = LOW) und es wird 50 Millisekunden gewartet. Dies verhindert ein lautes "Ploppen" in den Lautsprechern.
*   **Auto-Mute:** Sobald eine Datei zu Ende gespielt ist, zieht die kritische Loop-Logik den Shutdown-Pin automatisch wieder auf HIGH. Dadurch wird analoges Rauschen des Verstärkers im Leerlauf komplett unterbunden.
