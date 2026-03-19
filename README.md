# 🔊 Insane ESPH: ESP8266 Chime Component
<div align="center">
  <img src="https://img.shields.io/github/v/release/babeinlovexd/ESP8266-Chime?style=for-the-badge&color=2ecc71" alt="Latest Release">
  <img src="https://img.shields.io/badge/Status-Stable-2ecc71?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/ESPHome-Ready-03A9F4?style=for-the-badge&logo=esphome" alt="ESPHome">
  <img src="https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey?style=for-the-badge&logo=creative-commons" alt="License: CC BY-NC-SA 4.0">
</div>
<br>

Willkommen bei der **Insane ESPH: ESP8266 Chime Component** – deiner ultimativen Custom-Audio-Lösung für ESP8266 in Home Assistant!

Diese benutzerdefinierte (external component) ESPHome-Komponente wurde für das "Insane ESPH" Projekt entwickelt. Sie spielt **10 in PROGMEM gespeicherte WAV-Dateien** über I2S auf einem ESP8266 ab (unter Verwendung eines PT8211 DAC + LM4871 Verstärker) und bringt eine intelligente State Machine für Chime (Gong) und Alarm mit.

### 🔥 Was kann das Teil ALLES?
Dieses Plugin ist auf absolute Zuverlässigkeit und minimalen Aufwand ausgelegt:
* **Eigene C++ I2S-Wiedergabe:** Kein Rückgriff mehr auf fehleranfällige externe Bibliotheken (wie ESP8266Audio). Audio Playback läuft nativ über `<core_esp8266_i2s.h>` und `i2s_write_sample_nb()`. Dies sorgt für reibungslose PlatformIO-Kompilierungen und maximale Zuverlässigkeit ohne Dependency-Konflikte.
* **10 Integrierte PROGMEM Sounds:** Ding Dong, Trill Alarm, Sweep Sound, Solid Beep, G5 Chime, Siren, Doorbell, Notification, Error, Success. (Alle 8000Hz, Mono, als Hex-Arrays integriert).
* **Duale State Machine (Chime & Alarm):** Intelligente Prioritätssteuerung. Der Alarm hat **höchste Priorität** und loopt kontinuierlich, bis er manuell deaktiviert wird. Laufende Chimes (Gongs) werden sofort für den Alarm unterbrochen, und der Chime-Button wird während eines Alarms ignoriert.
* **Vollautomatische Home Assistant Integration:** Erstellt aus einer minimalen YAML-Konfiguration automatisch 7 Entitäten in Home Assistant. Keine versteckten Text-Sensoren, sondern saubere `number`, `select`, `button` und `switch` Sub-Entities.
* **Smarter Popschutz (Standby-Logik):** Steuert den Shutdown-Pin deines Verstärkers (LOW = an, HIGH = stumm) mit einem integrierten 50ms Delay vor der Wiedergabe, um Knack-Geräusche beim Einschalten zu vermeiden.
* **PT8211 DAC Kompatibilität:** 16-Bit Mono-Samples aus dem PROGMEM werden on-the-fly zu 32-Bit Stereo-Daten kombiniert, um den PT8211 DAC korrekt anzusteuern (Linker Kanal in den unteren 16 Bits, Rechter Kanal in den oberen 16 Bits).

---

## ✨ Automatisch erzeugte Entitäten in Home Assistant

Sobald das Gerät geflasht und mit Home Assistant verbunden ist, werden folgende 7 Entitäten vollautomatisch erzeugt und miteinander verknüpft:

* **Sektion 1 (Chime/Gong):**
  1. `number`: "Chime Lautstärke" (0-100%).
  2. `number`: "Chime Wiederholungen" (1-5x).
  3. `select`: "Chime Ton" (Auswahl aus 10 Sounds).
  4. `button`: "Chime Abspielen" (Startet den Gong).
* **Sektion 2 (Alarm):**
  5. `number`: "Alarm Lautstärke" (0-100%).
  6. `select`: "Alarm Ton" (Auswahl aus 10 Sounds).
  7. `switch`: "Alarm Loop" (Endlosschleife, bis der Schalter deaktiviert wird).

---

## 🛠️ Hardware-Verkabelung

> **⚠️ Wichtiger Hinweis zu den ESP8266 Pins:** Auf dem ESP8266 sind die I2S-Pins hardwareseitig **fest vorgegeben** und können nicht dynamisch neu zugewiesen werden!

Standard-Konfiguration des Projekts:

- **BCLK** (I2S Bit Clock) -> GPIO15 -> PT8211
- **WS** (I2S Word Select / LRCLK) -> GPIO2 -> PT8211
- **DOUT** (I2S Data Out / DIN/RX) -> GPIO3 -> PT8211
- **SD** (Shutdown Pin) -> GPIO12 -> LM4871 Verstärker (HIGH = stumm, LOW = an)

> **💡 WICHTIG - Logger Konfiguration:** Da GPIO3 (RX) von der I2S-Datenschnittstelle mitbenutzt wird, **muss** im Logger-Modul deiner ESPHome Config die Baudrate zwingend auf `0` gesetzt werden:
```yaml
logger:
  baud_rate: 0
```

---

## 💻 ESPHome YAML Konfiguration

Die Einbindung in deiner YAML bleibt erfreulich minimalistisch. Binde die Komponente als `external_components` direkt aus dem offiziellen GitHub-Repository ein und füge lediglich folgenden Block hinzu:

```yaml
logger:
  baud_rate: 0

external_components:
  - source:
      type: git
      url: https://github.com/babeinlovexd/ESP8266-Chime
      ref: main

esp8266_chime:
  id: my_chime
  bclk: GPIO15
  ws: GPIO2
  dout: GPIO3
  sd:
    number: GPIO12
    inverted: false

# Notwendig, damit die automatischen Entitäten von ESPHome generiert werden
number:
select:
button:
switch:
```

---

## ⚖️ Lizenz
Dieses komplette Projekt steht unter der [CC BY-NC-SA 4.0 Lizenz](https://creativecommons.org/licenses/by-nc-sa/4.0/).
Das bedeutet: Nachbauen und Anpassen für private Zwecke ist ausdrücklich erwünscht, jede kommerzielle Nutzung oder der Verkauf sind strikt verboten!

---

## ☕ Support dieses Projekts
Dieses Plugin hat extrem viel Zeit, Nerven und Kaffee gekostet. Wenn dir das System gefällt und du meine Arbeit unterstützen möchtest, freue ich mich riesig über einen virtuellen Kaffee!

<a href="https://www.paypal.me/babeinlovexd">
  <img src="https://img.shields.io/badge/Donate-PayPal-blue.svg?style=for-the-badge&logo=paypal" alt="Donate mit PayPal">
</a>

Jeder Cent fließt direkt in neue Entwicklungen und Hardware-Prototypen! 🚀

---

## 👨‍💻 Entwickelt von

| [<img src="https://avatars.githubusercontent.com/u/43302033?v=4" width="100"><br><sub>**Christopher**</sub>](https://github.com/babeinlovexd) |
| :---: |

---
