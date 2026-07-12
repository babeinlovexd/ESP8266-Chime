# 🔊 Insane ESPH: ESP8266 Chime Component
<div align="center">
  <img src="https://img.shields.io/github/v/release/babeinlovexd/ESP8266-Chime?style=for-the-badge&color=2ecc71" alt="Latest Release">
  <img src="https://img.shields.io/badge/Status-Stable-2ecc71?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/ESPHome-Ready-03A9F4?style=for-the-badge&logo=esphome" alt="ESPHome">
  <img src="https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey?style=for-the-badge&logo=creative-commons" alt="License: CC BY-NC-SA 4.0">
</div>
<br>

Willkommen bei der **Insane ESPH: ESP8266 Chime Component** – deiner ultimativen Custom-Audio-Lösung für ESP8266 in Home Assistant!

Diese benutzerdefinierte (external component) ESPHome-Komponente wurde für das "Insane ESPH" Projekt entwickelt. Sie spielt **30 in PROGMEM gespeicherte WAV-Dateien** über I2S auf einem ESP8266 ab (unter Verwendung eines PT8211 DAC + LM4871 Verstärker) und bringt eine intelligente State Machine für Chime (Gong) und Alarm mit.

### 🔥 Was kann das Teil ALLES?
Dieses Plugin ist auf absolute Zuverlässigkeit und minimalen Aufwand ausgelegt:
* **Eigene C++ I2S-Wiedergabe:** Kein Rückgriff mehr auf fehleranfällige externe Bibliotheken (wie ESP8266Audio). Audio Playback läuft nativ über `<core_esp8266_i2s.h>` und `i2s_write_sample_nb()`. Dies sorgt für reibungslose PlatformIO-Kompilierungen und maximale Zuverlässigkeit ohne Dependency-Konflikte.
* **14 Integrierte PROGMEM Sounds + 8 TTS Ansagen:**
  - **Standard & Alarm:** Ding Dong, Trill Alarm, Sweep Sound, G5 Chime, Doorbell, Pre Alarm.
  - **Sci-Fi / UI:** Notification Chime, Notification Bloop.
  - **Gaming & Specials:** Level Up, Coin, Glass Ping, Elevator Ding, Soft Bell, Magic Sparkle.
  - **Offline TTS Ansagen:** "Essen ist Fertig", "Waschmaschine ist fertig", "Trockner ist fertig", "Post ist da", "Schwarze Mülltonne muss raus", "Grüne Mülltonne muss raus", "Gelbe Mülltonne muss raus", "Glas muss raus".
  (Alle 8000Hz, Mono, als Hex-Arrays integriert - speziell für 1MB ESP8266 Speicher optimiert).
* **Tri-State Machine (Chime, Alarm & Notify):** Intelligente Prioritätssteuerung. Der Alarm hat **höchste Priorität** und loopt kontinuierlich, bis er manuell deaktiviert wird. Laufende Chimes (Gongs) oder TTS-Ansagen (Notify) werden sofort für den Alarm unterbrochen.
* **Offline Text-to-Speech (TTS):** Das System liefert mehrere fertig generierte, sprachliche Status-Ansagen als komprimierte 16-bit 8000Hz WAV-Dateien aus (z.B. "Essen ist fertig", "Waschmaschine ist fertig", etc.). Ideal für Smarthome-Updates ohne Cloud!
* **Vollautomatische Home Assistant Integration:** Erstellt aus einer minimalen YAML-Konfiguration vollautomatisch 10 Entitäten in Home Assistant. Komplett Plug & Play – keine zusätzlichen `number`, `select`, `button` oder `switch` Plattform-Blöcke in der YAML nötig!
* **Smarter Popschutz (Standby-Logik):** Steuert den Shutdown-Pin deines Verstärkers (LOW = an, HIGH = stumm) mit einem integrierten 50ms Delay vor der Wiedergabe, um Knack-Geräusche beim Einschalten zu vermeiden.
* **PT8211 DAC Kompatibilität:** 16-Bit Mono-Samples aus dem PROGMEM werden on-the-fly zu 32-Bit Stereo-Daten kombiniert, um den PT8211 DAC korrekt anzusteuern (Linker Kanal in den unteren 16 Bits, Rechter Kanal in den oberen 16 Bits).

---


## ✨ Automatisch erzeugte Entitäten in Home Assistant

Sobald das Gerät geflasht und mit Home Assistant verbunden ist, werden folgende 10 Entitäten vollautomatisch erzeugt und miteinander verknüpft:

* **Sektion 1 (Chime/Gong):**
  1. `number`: "Chime Lautstärke" (0-100%).
  2. `number`: "Chime Wiederholungen" (1-5x).
  3. `select`: "Chime Ton" (Auswahl aus 30 Sounds).
  4. `button`: "Chime Abspielen" (Startet den Gong).
  5. `switch`: "Chime Mute" (Gong lautlos schalten, LED blinkt trotzdem).
* **Sektion 2 (Alarm):**
  6. `number`: "Alarm Lautstärke" (0-100%).
  7. `select`: "Alarm Ton" (Auswahl aus 30 Sounds).
  8. `switch`: "Alarm Loop" (Endlosschleife, bis der Schalter deaktiviert wird).
* **Sektion 3 (Notify / TTS):**
  9. `number`: "Notify Lautstärke" (0-100%).
  10. `select`: "Notify Ton" (Wähle hier speziell die TTS Ansagen).
  11. `button`: "Notify Abspielen" (Spielt die Status-Ansage einmalig ab).
* **Sektion 4 (LED - optional):**
  12. `number`: "LED Blinkdauer" (Dauer in Sekunden).
  13. `switch`: "LED Aktivieren" (Aktiviert das Blinken).
  14. `select`: "LED Frequenz" (Blinkgeschwindigkeit on-the-fly einstellen: low, middle, high).

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

> **Wichtig für den Erhalt der Einstellungen nach einem Neustart:**
> Füge `restore_from_flash: true` in deinem `esp8266:` Block hinzu, da ansonsten die Zustände der Entitäten nach einem Neustart des ESP8266 aus dem flüchtigen RTC-Speicher verloren gehen.

```yaml
esp8266:
  board: d1_mini
  restore_from_flash: true

logger:
  baud_rate: 0

external_components:
  - source:
      type: git
      url: https://github.com/babeinlovexd/esp8266-chime
    components: [ esp8266_chime ]

esp8266_chime:
  id: my_chime
  bclk: GPIO15
  ws: GPIO2
  dout: GPIO3
  i2s_format: LSBJ # Auswahl: PHILIPS oder LSBJ (Standard ist PHILIPS)
  language: de # Auswahl: de oder en (Legt die Sprache der TTS Ansagen fest. Spart Speicherplatz!)
  sd:
    number: GPIO12
    inverted: false
  notify_volume:
    name: "Notify Lautstärke"
  notify_sound:
    name: "Notify Ton"
  notify_play:
    name: "Notify Abspielen"
  led: # Optional
    out: GPIO14
    frequenz:
      name: "LED Frequenz"
    duration:
      name: "LED Blinkdauer"
    activation:
      name: "LED Aktivieren"
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
