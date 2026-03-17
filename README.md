# Insane ESPH: ESP8266 Chime Component

Diese benutzerdefinierte (external component) ESPHome-Komponente wurde für das "Insane ESPH" Projekt entwickelt. Sie spielt 10 in PROGMEM gespeicherte WAV-Dateien über I2S auf einem ESP8266 ab (unter Verwendung eines PT8211 DAC + LM4871 Verstärker) und bringt eine intelligente State Machine für Chime (Gong) und Alarm mit.

## Funktionen

- **Eigene I2S-Wiedergabe:** Kein Rückgriff mehr auf fehleranfällige externe Bibliotheken (wie ESP8266Audio). Dies sorgt für reibungslose PlatformIO-Kompilierungen und maximale Zuverlässigkeit.
- **10 Integrierte Sounds:** Ding Dong, Trill Alarm, Sweep Sound, Solid Beep, G5 Chime, Siren, Doorbell, Notification, Error, Success.
- **Duale Sektionen (Chime & Alarm):**
  - **Alarm hat höchste Priorität:** Läuft der Alarm-Loop, wird der Chime-Button ignoriert. Laufende Chimes werden sofort für den Alarm unterbrochen.
- Erstellt **vollautomatisch 7 Home Assistant Entitäten**:
  - **Sektion 1 (Chime/Gong):**
    1. `number`: "Chime Lautstärke" (0-100%).
    2. `number`: "Chime Wiederholungen" (1-5x).
    3. `select`: "Chime Ton" (Auswahl aus 10 Sounds).
    4. `button`: "Chime Abspielen" (Startet den Gong).
  - **Sektion 2 (Alarm):**
    5. `number`: "Alarm Lautstärke" (0-100%).
    6. `select`: "Alarm Ton" (Auswahl aus 10 Sounds).
    7. `switch`: "Alarm Loop" (Endlosschleife, bis der Schalter deaktiviert wird).
- Steuerung des Verstärker-Shutdown-Pins (Low=an, High=stumm) mit integriertem 50ms Delay vor der Wiedergabe, um Knack-Geräusche (Popschutz) zu vermeiden.

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

Die Einbindung in deiner YAML bleibt erfreulich minimalistisch. Binde die Komponente als "external_components" in deine ESPHome Konfiguration ein (z.B. lokal oder direkt aus GitHub) und füge lediglich folgenden Block hinzu:

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

Sobald das Gerät geflasht und mit Home Assistant verbunden ist, werden automatisch alle 7 Entitäten erzeugt und miteinander verknüpft!
