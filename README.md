# Insane ESPH: ESP8266 Chime Component

Diese benutzerdefinierte (external component) ESPHome-Komponente wurde für das "Insane ESPH" Projekt entwickelt. Sie spielt 5 in PROGMEM gespeicherte WAV-Dateien über I2S auf einem ESP8266 ab (unter Verwendung eines PT8211 DAC + LM4871 Verstärker).

## Funktionen

- Automatische Einbindung von echten PROGMEM WAV-Dateien (Ding Dong, Trill Alarm, Sweep Sound, Solid Beep, G5 Chime).
- Erstellt automatisch Home Assistant Entitäten:
  - Ein **Number** (Slider) für die Lautstärkeregelung (0-100%).
  - Ein **Select** (Dropdown) zur Auswahl des Sounds.
  - Einen **Button**, der den gewählten Ton abspielt.
- Steuerung des Verstärker-Shutdown-Pins (Low=an, High=stumm) mit integriertem 50ms Delay vor der Wiedergabe, um Knack-Geräusche zu vermeiden.

## Hardware-Verkabelung

Die Pins können in ESPHome frei zugewiesen werden. Standard-Konfiguration des Projekts:

- **BCLK** (I2S Bit Clock) -> GPIO15 -> PT8211
- **WS** (I2S Word Select / LRCLK) -> GPIO2 -> PT8211
- **DOUT** (I2S Data Out / DIN) -> GPIO3 -> PT8211
- **SD** (Shutdown Pin) -> GPIO12 -> LM4871 (HIGH = stumm, LOW = an)

*Hinweis: Da GPIO3 (RX) für I2S Data verwendet wird, muss im Logger-Modul der ESPHome Config die Baudrate auf 0 gesetzt werden:*
```yaml
logger:
  baud_rate: 0
```

## ESPHome YAML Konfiguration

Binde die Komponente als "external_components" in deine ESPHome Konfiguration ein (z.B. lokal oder direkt aus GitHub) und füge folgenden Block hinzu:

```yaml
external_components:
  - source:
      type: local
      path: components

esp8266_chime:
  id: my_chime
  bclk: GPIO15
  ws: GPIO2
  dout: GPIO3
  sd:
    number: GPIO12
    inverted: false
```

Sobald das Gerät geflasht und mit Home Assistant verbunden ist, siehst du die 3 neuen Entitäten (Slider, Dropdown, Button) und kannst die Sounds direkt abspielen!

## Abhängigkeiten

Diese Komponente lädt automatisch die C++ Bibliothek `earlephilhower/ESP8266Audio`. Es ist keine weitere Konfiguration der Libraries in deiner YAML nötig.
