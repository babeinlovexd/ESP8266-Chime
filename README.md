<p align="center">
  <a href="https://github.com/babeinlovexd"><img src="https://raw.githubusercontent.com/babeinlovexd/babeinlovexd/main/bxd-github-header.svg" width="520" alt="BxD / BabeinlovexD"></a>
</p>

# ESP8266 Chime

[Fragen & Fehler](https://github.com/babeinlovexd/ESP8266-Chime/issues) · [Releases](https://github.com/babeinlovexd/ESP8266-Chime/releases)

Ein Gong- und Benachrichtigungsmodul für **ESP8266, ESPHome und Home Assistant**. Audiodaten liegen im Flash und werden über I2S ausgegeben; ein Streamingdienst ist für die Wiedergabe der eingebauten Töne nicht nötig.

## Funktionen

- **14 Signaltöne** für Gong und Alarm, darunter Ding Dong, Trill Alarm, Coin und Notification Chime.
- **8 vorproduzierte Statusansagen** in Deutsch oder Englisch. `language` wählt beim Kompilieren den Sprachsatz; dies ist keine freie Text-to-Speech-Synthese.
- Getrennte Lautstärken für Gong, Alarm und Ansagen; Gong-Wiederholungen und Alarm-Dauerschleife.
- Alarm hat Vorrang vor Gong und Ansagen.
- Optionaler LED-Ausgang mit Blinkdauer und Frequenzwahl.
- Gespeicherte Einstellungen werden über ESPHome-Preferences wiederhergestellt.

## Hardware

| Signal | ESP8266 | Anschluss im Referenzaufbau |
| :--- | :--- | :--- |
| BCLK | GPIO15 | I2S-Takt zum DAC |
| WS | GPIO2 | Word Select zum DAC |
| DOUT | GPIO3 | Daten zum DAC |
| SD | GPIO12 | Shutdown-Steuerung des Verstärkers |

Der Referenzaufbau verwendet **PT8211 und LM4871**. Die ESP8266-I2S-Pins sind hardwareseitig festgelegt. `logger.baud_rate: 0` verhindert die Nutzung von GPIO3 durch den seriellen Logger. `sd.inverted` und `i2s_format` müssen zur eigenen Schaltung passen.

## Installation

Ergänze deine bestehende ESPHome-Gerätekonfiguration um:

```yaml
logger:
  baud_rate: 0

external_components:
  - source:
      type: git
      url: https://github.com/babeinlovexd/ESP8266-Chime
      ref: Main
    components: [esp8266_chime]

esp8266_chime:
  id: my_chime
  bclk: GPIO15
  ws: GPIO2
  dout: GPIO3
  sd:
    number: GPIO12
    inverted: false
  i2s_format: LSBJ
  language: de
```

`PHILIPS` ist der Standardwert für `i2s_format`; im PT8211-Beispiel wird `LSBJ` gewählt. `language` akzeptiert `de` (Standard) und `en`. WLAN, verschlüsselte Native API und OTA ergänzt du passend zu deinem Gerät. Prüfe und kompiliere die Konfiguration in ESPHome, flashe den ESP8266 und füge ihn in Home Assistant hinzu.

Das vollständige lokale Build-Beispiel liegt in [test_chime.yaml](test_chime.yaml). Es lädt `components/` vom lokalen Dateisystem statt aus GitHub.

## Home-Assistant-Entitäten

Ohne LED werden **11 Entitäten** angelegt:

| Bereich | Entitäten |
| :--- | :--- |
| Gong | Lautstärke, Wiederholungen, Ton, Abspielen, Mute |
| Alarm | Lautstärke, Ton, Loop |
| Ansagen | Lautstärke, Ansage, Abspielen |

Mit dem optionalen `led`-Block kommen **3 weitere Entitäten** hinzu:

```yaml
# Innerhalb von esp8266_chime ergänzen:
  led:
    out: GPIO14
    frequenz:
      name: "LED Frequenz"
    duration:
      name: "LED Blinkdauer"
    activation:
      name: "LED Aktivieren"
```

`duration` lässt sich von 1 bis 15 Sekunden einstellen; `frequenz` bietet `low`, `middle` und `high`. Eigene Namen können auch für die übrigen Entitäten im Komponentenblock vergeben werden.

## Eigene Sounds & Fehlersuche

[generate_sounds.py](generate_sounds.py) und [generate_tts.py](generate_tts.py) erzeugen die eingebetteten Audiodaten. Änderungen daran benötigen einen neuen Firmware-Build; es gibt keinen Sound-Upload zur Laufzeit.

- **Kein Ton:** DAC-Verkabelung, gemeinsame Masse, Verstärker-Shutdown und I2S-Format prüfen.
- **GPIO-Konflikt:** Seriellen Logger deaktivieren und GPIO15/2/3 für I2S freihalten.
- **Gong wird unterbrochen:** Prüfen, ob die höher priorisierte Alarm-Dauerschleife aktiv ist.
- **Geänderte Sounds fehlen:** Firmware neu kompilieren und flashen; die Dateien liegen im Programmspeicher.

## Lizenz

[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Es gilt die bestehende Projektlizenz. Eingebundene Drittanbieter-Komponenten behalten ihre jeweiligen Lizenzen.

---

## Builds und Releases

Version: **1.3.4** ([VERSION](VERSION)). [GitHub Actions](.github/workflows/release.yml) prüft Pushes und Pull Requests. Ein Tag passend zu `v` + `VERSION` veröffentlicht das Release erst nach erfolgreichen Jobs; manuelle Läufe liefern Build-Artefakte. [Downloads](https://github.com/babeinlovexd/ESP8266-Chime/releases).

ESPHome-CI verwendet Platzhalter-Zugangsdaten und flasht keine Geräte. Vor dem Einsatz eigene Secrets und Pinbelegung prüfen.

## Mitmachen

Fragen, Fehlerberichte und Beiträge sind willkommen. Nenne bei einem [Issue](https://github.com/babeinlovexd/ESP8266-Chime/issues) bitte Version, Aufbau und Schritte zum Nachstellen. Größere Änderungen besprechen wir am besten vor einem Pull Request.

Wenn du dieses Hobbyprojekt unterstützen möchtest: [PayPal](https://www.paypal.me/babeinlovexd).

[BxD / BabeinlovexD](https://github.com/babeinlovexd) · [Website](https://babeinlovexd.de/)
